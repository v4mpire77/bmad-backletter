from fastapi import APIRouter
from typing import Any, Dict, List

from ..services.rulepack_loader import load_rulepacks

router = APIRouter()


def load_rulepack():
    packs = load_rulepacks()
    return packs[0] if packs else None


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for rules module."""
    return {"status": "ok", "module": "rules"}


@router.get("/rules/summary")
async def rules_summary() -> Dict[str, Any]:
    rp = load_rulepack()
    if rp is None:
        return {"name": "", "version": "", "detector_count": 0, "detectors": [], "lexicons": []}
    return {
        "name": getattr(rp, "name", getattr(rp, "id", "")),
        "version": getattr(rp, "version", ""),
        "detector_count": len(getattr(rp, "detectors", [])),
        "detectors": [
            {
                "id": getattr(d, "id", ""),
                "type": getattr(d, "type", ""),
                "description": getattr(d, "description", None),
                "lexicon": getattr(d, "lexicon", None),
            }
            for d in getattr(rp, "detectors", [])
        ],
        "lexicons": list(getattr(rp, "lexicons", {}).keys()),
    }

