from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

from ..models.schemas import Finding
from ..services import storage

router = APIRouter(tags=["docs"])


@router.get("/docs/{doc_id}/findings", response_model=List[Finding])
def get_doc_findings(doc_id: str) -> List[Finding]:
    data = storage.get_analysis_findings(doc_id)
    if not data:
        raise HTTPException(
            status_code=404,
            detail={"code": "not_found", "message": "Document not found"},
        )
    return [Finding(**f) for f in data]
