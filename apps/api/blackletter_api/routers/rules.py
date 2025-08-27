from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..services.rulepack_loader import RulepackError, load_rulepack


router = APIRouter(tags=["rules"])


@router.get("/rules/summary")
def get_rules_summary():
    try:
        rp = load_rulepack()
    except RulepackError as e:
        raise HTTPException(status_code=500, detail=f"Rulepack error: {e}")

    return {
        "name": rp.name,
        "version": rp.version,
        "detector_count": len(rp.detectors),
        "detectors": [
            {
                "id": d.id,
                "type": d.type,
                "description": d.description,
                "lexicon": d.lexicon,
            }
            for d in rp.detectors
        ],
        "lexicons": sorted(list(rp.lexicons.keys())),
    }

