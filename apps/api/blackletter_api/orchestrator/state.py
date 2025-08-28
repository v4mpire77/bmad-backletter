from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any
from uuid import uuid4


class AnalysisState(str, Enum):
    RECEIVED = "RECEIVED"
    EXTRACTED = "EXTRACTED"
    SEGMENTED = "SEGMENTED"
    GDPR_DONE = "GDPR_DONE"
    LEGAL_DONE = "LEGAL_DONE"
    GC_DONE = "GC_DONE"
    REPORTED = "REPORTED"


@dataclass
class AnalysisRecord:
    id: str
    filename: str
    state: AnalysisState = AnalysisState.RECEIVED
    findings: List[Dict[str, Any]] = field(default_factory=list)


class Orchestrator:
    """In-memory orchestrator for analysis state transitions."""

    def __init__(self) -> None:
        self._store: Dict[str, AnalysisRecord] = {}

    def intake(self, filename: str) -> str:
        analysis_id = str(uuid4())
        self._store[analysis_id] = AnalysisRecord(id=analysis_id, filename=filename)
        return analysis_id

    def summary(self, analysis_id: str) -> AnalysisRecord:
        return self._store[analysis_id]

    def findings(self, analysis_id: str) -> List[Dict[str, Any]]:
        return self._store[analysis_id].findings

    def list_records(self, limit: int) -> List[AnalysisRecord]:
        return list(self._store.values())[:limit]


# module-level orchestrator instance
orchestrator = Orchestrator()
