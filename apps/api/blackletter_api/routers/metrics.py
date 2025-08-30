from __future__ import annotations

from fastapi import APIRouter

from ..services.job_store import job_store

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
async def get_metrics() -> dict:
    return await job_store.stats()

