from __future__ import annotations

from datetime import datetime, timezone
from typing import List

import os
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..models.schemas import AnalysisSummary, Finding, VerdictCounts
from ..services import storage
from ..orchestrator.state import orchestrator


router = APIRouter(tags=["analyses"])


class IntakeRequest(BaseModel):
    filename: str


@router.post("/intake")
def intake(req: IntakeRequest) -> dict:
    analysis_id = orchestrator.intake(req.filename)
    return {"analysis_id": analysis_id}


@router.get("/analyses", response_model=List[AnalysisSummary])
def list_analyses(limit: int = Query(default=50, ge=1, le=200)) -> List[AnalysisSummary]:
    # If FS-backed listing is enabled, read summaries from disk;
    # otherwise, surface in-memory orchestrator records.
    if os.getenv("ANALYSES_FS_ENABLED", "0") == "1":
        fs_items = storage.list_analyses_summaries(limit=limit)
        # Ensure required 'state' is present on each item.
        enriched: List[AnalysisSummary] = []
        for it in fs_items:
            enriched.append(
                AnalysisSummary(
                    id=it.id,
                    filename=it.filename,
                    created_at=it.created_at,
                    size=it.size,
                    state=getattr(it, "state", "REPORTED"),
                    verdicts=it.verdicts,
                )
            )
        return enriched

    summaries: List[AnalysisSummary] = []
    for rec in orchestrator.list_records(limit):
        summaries.append(
            AnalysisSummary(
                id=rec.id,
                filename=rec.filename,
                created_at=datetime.now(timezone.utc).isoformat(),
                size=0,
                state=rec.state.value,
                verdicts=VerdictCounts(),
            )
        )
    return summaries


@router.get("/analyses/{analysis_id}", response_model=AnalysisSummary)
def get_analysis_summary(analysis_id: str) -> AnalysisSummary:
    """Get analysis summary with Story 4.2 coverage information."""
    try:
        rec = orchestrator.summary(analysis_id)
        
        # Get findings to compute coverage
        try:
            rec_findings = orchestrator.findings(analysis_id)
            findings_list = [f for f in rec_findings]
        except Exception:
            findings_list = []
        
        # Compute coverage using Story 4.2 service
        from ..services.coverage import compute_analysis_coverage
        coverage = compute_analysis_coverage(analysis_id, findings_list)
        
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail={"code": "not_found", "message": "Analysis not found"},
        ) from exc
    
    return AnalysisSummary(
        id=rec.id,
        filename=rec.filename,
        created_at=datetime.now(timezone.utc).isoformat(),
        size=0,
        state=rec.state.value,
        verdicts=VerdictCounts(),
        coverage=coverage  # Story 4.2 - Include coverage
    )


@router.get("/analyses/{analysis_id}/findings", response_model=List[Finding])
def get_analysis_findings(analysis_id: str) -> List[Finding]:
    try:
        rec_findings = orchestrator.findings(analysis_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail={"code": "not_found", "message": "Analysis not found"},
        ) from exc
    enriched = []
    for f in rec_findings:
        enriched.append(
            {
                **f,
                "rule_id": f.get("rule_id") or f.get("detector_id", ""),
                "original_text": f.get("original_text") or f.get("snippet", ""),
                "suggested_text": f.get("suggested_text") or f.get("snippet", ""),
            }
        )
    return [Finding(**f) for f in enriched]
