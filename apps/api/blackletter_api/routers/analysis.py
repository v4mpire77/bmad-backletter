from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..models.schemas import Finding
from ..services.analysis_orchestrator import run_analysis
from ..services.rulepack_loader import load_rulepack

router = APIRouter(tags=["analysis"])


class DetectRequest(BaseModel):
    text: str


@router.post("/analysis/{doc_id}/detect", response_model=List[Finding])
def detect(doc_id: str, req: DetectRequest) -> List[Finding]:
    rulepack = load_rulepack()
    if rulepack is None:
        raise HTTPException(
            status_code=500,
            detail={"code": "rulepack_missing", "message": "No rulepack loaded"},
        )
    return run_analysis(req.text, rulepack)
