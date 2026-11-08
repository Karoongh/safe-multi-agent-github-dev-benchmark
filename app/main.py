import codecs
import os
import re
import unicodedata
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

UPLOAD_DIR = Path("uploads")
MAX_UPLOAD_SIZE = 10 * 1024 * 1024
CHUNK_SIZE = 64 * 1024

ALLOWED_TYPES = {
    ".txt": "text/plain",
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}
SIGNATURES = {
    ".pdf": lambda data: data.startswith(b"%PDF-"),
    ".png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
    ".jpg": lambda data: data.startswith(b"\xff\xd8\xff"),
    ".jpeg": lambda data: data.startswith(b"\xff\xd8\xff"),
}
WINDOWS_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}

app = FastAPI(title="Secure File Upload Benchmark")


def normalize_filename(filename: str) -> str:
    """Return a safe, portable basename; never use a client-supplied path."""
    normalized = unicodedata.normalize("NFKC", filename).replace("\\", "/")
    basename = normalized.rsplit("/", 1)[-1].strip(" .")
    if not basename or basename in {".", ".."}:
        raise HTTPException(status_code=400, detail="Invalid filename")

    basename = re.sub(r"[^\w.-]", "_", basename, flags=re.UNICODE)
    basename = basename.lstrip(".").strip()
    if not basename or basename in {".", ".."}:
        raise HTTPException(status_code=400, detail="Invalid filename")

    suffix = Path(basename).suffix.lower()
    stem = basename[:-len(Path(basename).suffix)] if Path(basename).suffix else basename
    if not stem or stem.upper() in WINDOWS_RESERVED_NAMES:
        raise HTTPException(status_code=400, detail="Invalid filename")
    if suffix not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    # Keep names bounded and avoid pathological filesystem names.
    stem = stem[:100]
    return f"{stem}{suffix}"


def _open_unique_destination(directory: Path, filename: str):
    """Create a file without overwriting an existing upload."""
    candidate = Path(filename)
    stem, suffix = candidate.stem, candidate.suffix
    for attempt in range(10):
        name = filename if attempt == 0 else f"{stem}-{uuid.uuid4().hex[:8]}{suffix}"
        path = directory / name
        try:
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            return descriptor, name, path
        except FileExistsError:
            continue
    raise HTTPException(status_code=409, detail="Could not allocate a unique filename")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    safe_filename = normalize_filename(file.filename)
    extension = Path(safe_filename).suffix
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    descriptor, stored_filename, destination = _open_unique_destination(
        UPLOAD_DIR, safe_filename
    )
    total_size = 0
    header = bytearray()
    text_decoder = codecs.getincrementaldecoder("utf-8")() if extension == ".txt" else None

    try:
        with os.fdopen(descriptor, "wb") as output:
            while True:
                chunk = await file.read(CHUNK_SIZE)
                if not chunk:
                    break

                total_size += len(chunk)
                if total_size > MAX_UPLOAD_SIZE:
                    raise HTTPException(status_code=413, detail="File is too large")

                if len(header) < 16:
                    header.extend(chunk[: 16 - len(header)])

                if text_decoder is not None:
                    try:
                        decoded = text_decoder.decode(chunk)
                    except UnicodeDecodeError as exc:
                        raise HTTPException(status_code=415, detail="Invalid text encoding") from exc
                    if "\x00" in decoded:
                        raise HTTPException(status_code=415, detail="Unsupported text content")

                output.write(chunk)

            if extension in SIGNATURES and not SIGNATURES[extension](bytes(header)):
                raise HTTPException(status_code=415, detail="File content does not match its extension")
            if text_decoder is not None:
                try:
                    text_decoder.decode(b"", final=True)
                except UnicodeDecodeError as exc:
                    raise HTTPException(status_code=415, detail="Invalid text encoding") from exc

        return {
            "filename": stored_filename,
            "size": total_size,
            "content_type": ALLOWED_TYPES[extension],
        }
    except Exception:
        destination.unlink(missing_ok=True)
        raise
