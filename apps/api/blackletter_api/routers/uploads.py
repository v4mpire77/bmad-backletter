from __future__ import annotations

from fastapi import APIRouter, File, UploadFile

from ..models.job import JobCreateResponse
from ..services.upload_orchestrator import submit_upload

router = APIRouter(tags=["uploads"])


@router.post("/uploads", response_model=JobCreateResponse)
async def create_upload(file: UploadFile = File(...)) -> JobCreateResponse:
    job = await submit_upload(file=file)
    return JobCreateResponse(job_id=job.id)

