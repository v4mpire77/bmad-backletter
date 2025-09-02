from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import threading
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
    """In-memory orchestrator for analysis state transitions.

    This orchestrator maintains state in-process and guards access with a
    :class:`threading.Lock` for thread safety. It is not suitable for
    multi-process deployments.
    """

    def __init__(self) -> None:
        self._store: Dict[str, AnalysisRecord] = {}
        self._lock = threading.Lock()

    def intake(self, filename: str) -> str:
        with self._lock:
            analysis_id = str(uuid4())
            self._store[analysis_id] = AnalysisRecord(id=analysis_id, filename=filename)
            return analysis_id

    def summary(self, analysis_id: str) -> AnalysisRecord:
        with self._lock:
            return self._store[analysis_id]

    def findings(self, analysis_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            return self._store[analysis_id].findings

    def advance(
        self,
        analysis_id: str,
        new_state: AnalysisState,
        finding: Dict[str, Any] | None = None,
    ) -> AnalysisRecord:
        """Update the state of an analysis and optionally append a finding.

        Args:
            analysis_id: Identifier returned by :meth:`intake`.
            new_state: The next :class:`AnalysisState` to assign.
            finding: Optional detail to add to the record's findings list.

        Returns:
            The updated :class:`AnalysisRecord` instance.
        """

        with self._lock:
            record = self._store[analysis_id]
            record.state = new_state
            if finding:
                record.findings.append(finding)
            return record

    def list_records(self, limit: int) -> List[AnalysisRecord]:
        with self._lock:
            return list(self._store.values())[:limit]


# module-level orchestrator instance
orchestrator = Orchestrator()
