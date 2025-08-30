from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..models.job import JobCreateResponse
from ..services.upload_orchestrator import submit_upload

router = APIRouter(tags=["uploads"])


ALLOWED_MIME_TYPES = {
    "text/plain",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

# 10 MiB limit
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


@router.post("/uploads", response_model=JobCreateResponse)
async def create_upload(file: UploadFile = File(...)) -> JobCreateResponse:
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="unsupported mime type")

    # Size validation: read up to limit+1 without persisting content, then rewind.
    bytes_read = 0
    limit = MAX_UPLOAD_BYTES
    chunk_size = 1024 * 256  # 256 KiB
    while True:
        chunk = await file.read(min(chunk_size, limit - bytes_read + 1))
        if not chunk:
            break
        bytes_read += len(chunk)
        if bytes_read > limit:
            await file.close()
            raise HTTPException(status_code=413, detail="file too large")
        if bytes_read == limit:
            # read one more byte to detect overflow on next loop
            continue
    # Rewind so downstream processors can read if needed
    try:
        file.file.seek(0)
    except Exception:
        pass

    job = await submit_upload(file=file)
    return JobCreateResponse(job_id=job.id)
