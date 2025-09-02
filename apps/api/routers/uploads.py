from __future__ import annotations

from uuid import uuid4
from typing import Dict

from fastapi import APIRouter, File, HTTPException, UploadFile

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

jobs_store: Dict[str, str] = {}

router = APIRouter()


@router.post("/docs/upload")
async def upload_document(file: UploadFile = File(...)) -> dict[str, str]:
    contents = await file.read()
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    job_id = str(uuid4())
    analysis_id = str(uuid4())
    jobs_store[job_id] = "queued"
    return {"job_id": job_id, "analysis_id": analysis_id, "status": "queued"}
