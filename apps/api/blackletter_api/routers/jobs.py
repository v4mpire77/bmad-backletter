from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..models.job import Job
from ..services.job_store import job_store

router = APIRouter(tags=["jobs"])


@router.get("/jobs/{job_id}", response_model=Job)
async def get_job(job_id: str) -> Job:
    job = await job_store.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return job

