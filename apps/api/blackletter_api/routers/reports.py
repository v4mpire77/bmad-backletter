from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import database
from ..models.entities import Report
from ..models.schemas import ReportExport, ExportOptions

router = APIRouter(tags=["reports"])


@router.get("/reports", response_model=List[ReportExport])
def list_reports(db: Session = Depends(database.get_db)) -> List[ReportExport]:
    reports = db.query(Report).order_by(Report.created_at.desc()).all()
    return [
        ReportExport(
            id=str(r.id),
            analysis_id=r.analysis_id,
            filename=r.filename,
            created_at=r.created_at.isoformat(),
            options=ExportOptions(**r.options),
        )
        for r in reports
    ]


@router.post("/reports/{analysis_id}", response_model=ReportExport, status_code=status.HTTP_201_CREATED)
def create_report(analysis_id: str, opts: ExportOptions, db: Session = Depends(database.get_db)) -> ReportExport:
    report = Report(
        analysis_id=analysis_id,
        filename=f"{analysis_id.upper()}.pdf",
        options=opts.dict(),
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return ReportExport(
        id=str(report.id),
        analysis_id=report.analysis_id,
        filename=report.filename,
        created_at=report.created_at.isoformat(),
        options=opts,
    )
