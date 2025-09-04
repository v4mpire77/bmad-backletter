from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..services.rulepack_loader import load_rulepack, RulepackError
from ..models.schemas import RulesSummary, DetectorSummary

router = APIRouter(prefix="/rules", tags=["rules"])


@router.get("/summary")
def rules_summary() -> dict:
    try:
        rp = load_rulepack()
        if not rp:
            raise RulepackError("no rulepack loaded")
    except RulepackError as e:
        raise HTTPException(status_code=500, detail=f"Rulepack error: {e}")

    detectors = [
        DetectorSummary(
            id=getattr(d, "id", ""),
            type=getattr(d, "type", "lexicon"),
            description=getattr(d, "description", None),
            lexicon=getattr(d, "lexicon", None),
        )
        for d in (rp.detectors or [])
    ]
    summary = RulesSummary(
        name=getattr(rp, "name", "unknown"),
        version=getattr(rp, "version", "v0"),
        detector_count=len(detectors),
        detectors=detectors,
        lexicons=sorted(list((rp.lexicons or {}).keys())),
    )
    return summary.model_dump()
