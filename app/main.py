from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Secure File Upload Benchmark")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    # Intentionally incomplete starter implementation.
    # The benchmark task asks the agent to address upload safety and scalability.
    destination = UPLOAD_DIR / file.filename
    data = await file.read()
    destination.write_bytes(data)

    return {
        "filename": file.filename,
        "size": len(data),
        "content_type": file.content_type,
    }
