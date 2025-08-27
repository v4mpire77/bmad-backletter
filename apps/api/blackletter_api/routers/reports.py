from __future__ import annotations

from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from fastapi import APIRouter, status

from ..models.schemas import ReportExport, ExportOptions

router = APIRouter(tags=["reports"])

_exports: List[ReportExport] = []


@router.get("/reports", response_model=List[ReportExport])
def list_reports() -> List[ReportExport]:
    return _exports


@router.post("/reports/{analysis_id}", response_model=ReportExport, status_code=status.HTTP_201_CREATED)
def create_report(analysis_id: str, opts: ExportOptions) -> ReportExport:
    rec = ReportExport(
        id=str(uuid4()),
        analysis_id=analysis_id,
        filename=f"{analysis_id.upper()}.pdf",
        created_at=datetime.now(timezone.utc).isoformat(),
        options=opts,
    )
    _exports.insert(0, rec)
    del _exports[20:]
    return rec
