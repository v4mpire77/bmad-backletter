from __future__ import annotations

import uuid
from typing import Dict

from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models.entities import ExtractionArtifact, EvidenceArtifact


def record_extraction_artifact(
    analysis_id: str,
    job_id: str,
    artifact_path: str,
    db: Session | None = None,
) -> ExtractionArtifact:
    """Persist a reference to an extraction artifact on disk."""
    owns = False
    if db is None:
        db = SessionLocal()
        owns = True
    try:
        art = ExtractionArtifact(
            analysis_id=uuid.UUID(analysis_id),
            job_id=uuid.UUID(job_id),
            artifact_path=artifact_path,
        )
        db.add(art)
        db.commit()
        db.refresh(art)
        return art
    finally:
        if owns:
            db.close()


def record_evidence_artifact(
    analysis_id: str,
    job_id: str,
    window: Dict,
    db: Session | None = None,
) -> EvidenceArtifact:
    """Store an evidence window snippet for a finding."""
    owns = False
    if db is None:
        db = SessionLocal()
        owns = True
    try:
        art = EvidenceArtifact(
            analysis_id=uuid.UUID(analysis_id),
            job_id=uuid.UUID(job_id),
            snippet=window.get("snippet", ""),
            page=int(window.get("page", 0)),
            start=int(window.get("start", 0)),
            end=int(window.get("end", 0)),
        )
        db.add(art)
        db.commit()
        db.refresh(art)
        return art
    finally:
        if owns:
            db.close()
