from __future__ import annotations

from fastapi import APIRouter

from ..services.rulepack_loader import api_rules_summary

router = APIRouter(prefix="/rules", tags=["rules"])


@router.get("/summary")
def rules_summary() -> dict:
    return api_rules_summary()
