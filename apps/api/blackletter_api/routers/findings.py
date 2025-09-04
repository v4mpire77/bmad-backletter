from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, Query

from ..models.schemas import Finding
from ..services.tasks import get_job
from ..services import storage

router = APIRouter(tags=["findings"])


@router.get("/findings", response_model=List[Finding])
def get_findings(job_id: str = Query(...)) -> List[Finding]:
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="not_found")
    data = storage.get_analysis_findings(job.analysis_id)
    enriched = []
    for f in data:
        enriched.append(
            {
                **f,
                "rule_id": f.get("rule_id") or f.get("detector_id", ""),
                "original_text": f.get("original_text") or f.get("snippet", ""),
                "suggested_text": f.get("suggested_text") or f.get("snippet", ""),
            }
        )
    return [Finding(**f) for f in enriched]
