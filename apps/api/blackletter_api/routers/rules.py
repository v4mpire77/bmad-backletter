from fastapi import APIRouter

from ..models.schemas import DetectorSummary, RulesSummary
from ..services.rulepack_loader import load_rulepack

router = APIRouter(tags=["rules"])


@router.get("/rules/summary", response_model=RulesSummary)
def rules_summary() -> RulesSummary:
    rp = load_rulepack()
    detectors = [
        DetectorSummary(
            id=d.id,
            type=d.type,
            description=d.description,
            lexicon=d.lexicon,
        )
        for d in rp.detectors
    ]
    return RulesSummary(
        name=rp.name,
        version=rp.version,
        detector_count=len(rp.detectors),
        detectors=detectors,
        lexicons=list(rp.lexicons.keys()),
    )
