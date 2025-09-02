from fastapi import APIRouter, HTTPException

from ..services.jobs_store import jobs_store

router = APIRouter()


@router.get("/jobs/{job_id}")
async def get_job(job_id: str) -> dict[str, str]:
    status = jobs_store.get(job_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status}
