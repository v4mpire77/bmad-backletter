from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Query

from ..models.schemas import AnalysisSummary, Finding, VerdictCounts


router = APIRouter(tags=["analyses"])


@router.get("/analyses", response_model=List[AnalysisSummary])
def list_analyses(limit: int = Query(default=50, ge=1, le=200)) -> List[AnalysisSummary]:
    # MVP scaffold: return an empty list until persistence is implemented.
    # Later: read from DB and/or filesystem under .data/analyses/...
    return []


@router.get("/analyses/{analysis_id}", response_model=AnalysisSummary)
def get_analysis_summary(analysis_id: str) -> AnalysisSummary:
    # Placeholder summary with stable shape for UI wiring
    return AnalysisSummary(
        id=analysis_id,
        filename="placeholder.pdf",
        created_at=datetime.now(timezone.utc).isoformat(),
        size=0,
        verdicts=VerdictCounts(),
    )


@router.get("/analyses/{analysis_id}/findings", response_model=List[Finding])
def get_analysis_findings(analysis_id: str) -> List[Finding]:
    # Placeholder: empty findings array
    return []
