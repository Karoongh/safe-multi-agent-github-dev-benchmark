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

ALLOWED_CONTENT_TYPES = {
    ".txt": "text/plain",
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}
SIGNATURE_CHECKS = {
    ".pdf": lambda data: data.startswith(b"%PDF-"),
    ".png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
    ".jpg": lambda data: data.startswith(b"\xff\xd8\xff"),
    ".jpeg": lambda data: data.startswith(b"\xff\xd8\xff"),
}
_RESERVED_NAMES = {
    "CON", "PRN", "AUX", "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}

app = FastAPI(title="Secure File Upload Benchmark")


def _safe_filename(client_filename: str) -> str:
    """Normalize an untrusted client filename to a safe basename."""
    normalized = unicodedata.normalize("NFKC", client_filename).replace("\\", "/")
    basename = normalized.rsplit("/", 1)[-1].strip(" .")
    if not basename or basename in {".", ".."}:
        raise HTTPException(status_code=400, detail="Invalid filename")

    basename = re.sub(r"[^\w.-]", "_", basename, flags=re.UNICODE).lstrip(".")
    if not basename or basename in {".", ".."}:
        raise HTTPException(status_code=400, detail="Invalid filename")

    original_suffix = Path(basename).suffix
    suffix = original_suffix.lower()
    stem = basename[:-len(original_suffix)] if original_suffix else basename
    if not stem or stem.upper() in _RESERVED_NAMES:
        raise HTTPException(status_code=400, detail="Invalid filename")
    if suffix not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    return f"{stem[:100]}{suffix}"


def _create_destination(directory: Path, filename: str):
    """Create a unique file atomically without overwriting an existing upload."""
    path = Path(filename)
    for attempt in range(10):
        candidate = filename if attempt == 0 else (
            f"{path.stem}-{uuid.uuid4().hex[:8]}{path.suffix}"
        )
        destination = directory / candidate
        try:
            descriptor = os.open(
                destination,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
            )
            return descriptor, candidate, destination
        except FileExistsError:
            continue
    raise HTTPException(status_code=409, detail="Unable to allocate a filename")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    safe_name = _safe_filename(file.filename)
    extension = Path(safe_name).suffix
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    descriptor, stored_name, destination = _create_destination(UPLOAD_DIR, safe_name)
    total_size = 0
    header = bytearray()
    text_decoder = codecs.getincrementaldecoder("utf-8")() if extension == ".txt" else None

    try:
        with os.fdopen(descriptor, "wb") as output:
            while chunk := await file.read(CHUNK_SIZE):
                total_size += len(chunk)
                if total_size > MAX_UPLOAD_SIZE:
                    raise HTTPException(status_code=413, detail="File exceeds the 10 MiB limit")

                if len(header) < 16:
                    header.extend(chunk[: 16 - len(header)])

                if text_decoder is not None:
                    try:
                        decoded = text_decoder.decode(chunk)
                    except UnicodeDecodeError as exc:
                        raise HTTPException(status_code=415, detail="Text file must be UTF-8") from exc
                    if "\x00" in decoded:
                        raise HTTPException(status_code=415, detail="Unsupported text content")

                output.write(chunk)

            if extension in SIGNATURE_CHECKS and not SIGNATURE_CHECKS[extension](bytes(header)):
                raise HTTPException(status_code=415, detail="File signature does not match extension")

            if text_decoder is not None:
                try:
                    text_decoder.decode(b"", final=True)
                except UnicodeDecodeError as exc:
                    raise HTTPException(status_code=415, detail="Text file must be UTF-8") from exc

        return {
            "filename": stored_name,
            "size": total_size,
            "content_type": ALLOWED_CONTENT_TYPES[extension],
        }
    except Exception:
        destination.unlink(missing_ok=True)
        raise
