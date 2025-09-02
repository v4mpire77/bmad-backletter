from __future__ import annotations

from pathlib import Path
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database
from ..models.entities import Analysis, Report
from ..models.schemas import ExportOptions, ReportExport
from ..services.reports import generate_report_pdf

router = APIRouter(tags=["reports"])


@router.get("/reports", response_model=List[ReportExport])
def list_reports(db: Session = Depends(database.get_db)) -> List[ReportExport]:
    reports = db.query(Report).order_by(Report.created_at.desc()).all()
    return [
        ReportExport(
            id=str(r.id),
            analysis_id=r.analysis_id,
            filename=r.filename,
            file_path=r.file_path,
            created_at=r.created_at.isoformat(),
            options=ExportOptions(**r.options),
        )
        for r in reports
    ]


@router.post("/reports/{analysis_id}", response_model=ReportExport, status_code=status.HTTP_201_CREATED)
def create_report(
    analysis_id: str, opts: ExportOptions, db: Session = Depends(database.get_db)
) -> ReportExport:
    try:
        analysis_uuid = UUID(analysis_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid analysis id") from e

    analysis = db.query(Analysis).filter(Analysis.id == analysis_uuid).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    output_path = reports_dir / f"{analysis_id.upper()}.pdf"
    generate_report_pdf(analysis, output_path)

    report = Report(
        analysis_id=analysis_id,
        filename=output_path.name,
        file_path=str(output_path),
        options=opts.dict(),
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return ReportExport(
        id=str(report.id),
        analysis_id=report.analysis_id,
        filename=report.filename,
        file_path=report.file_path,
        created_at=report.created_at.isoformat(),
        options=opts,
    )
