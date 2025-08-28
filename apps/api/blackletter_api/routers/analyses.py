from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List

from fastapi import APIRouter, HTTPException, Query

from ..models.schemas import AnalysisSummary, VerdictCounts
from ..orchestrator.state import orchestrator


router = APIRouter(tags=["analyses"])


def _to_summary(analysis) -> AnalysisSummary:
    return AnalysisSummary(
        id=analysis.id,
        filename="placeholder.pdf",
        created_at=datetime.now(timezone.utc).isoformat(),
        size=0,
        verdicts=VerdictCounts(),
        state=analysis.state,
    )


@router.get("/analyses", response_model=List[AnalysisSummary])
def list_analyses(limit: int = Query(default=50, ge=1, le=200)) -> List[AnalysisSummary]:
    analyses = list(orchestrator._analyses.values())[:limit]
    return [_to_summary(a) for a in analyses]


@router.post("/intake", response_model=AnalysisSummary)
def intake() -> AnalysisSummary:
    analysis = orchestrator.create()
    return _to_summary(analysis)


@router.get("/analyses/{analysis_id}", response_model=AnalysisSummary)
def get_analysis_summary(analysis_id: str) -> AnalysisSummary:
    analysis = orchestrator.get(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="analysis not found")
    return _to_summary(analysis)


@router.get("/analyses/{analysis_id}/findings", response_model=Dict[str, List[dict]])
def get_analysis_findings(analysis_id: str) -> Dict[str, List[dict]]:
    analysis = orchestrator.get(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="analysis not found")
    return analysis.findings
