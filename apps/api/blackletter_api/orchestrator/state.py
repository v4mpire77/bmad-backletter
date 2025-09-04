from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import threading
from typing import Dict, List, Any, Callable
from uuid import uuid4


class AnalysisState(str, Enum):
    """Possible states of an analysis."""

    # High level progress states for WebSocket updates
    QUEUED = "queued"
    EXTRACTING = "extracting"
    DETECTING = "detecting"
    REPORTING = "reporting"
    DONE = "done"

    # Legacy internal states
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
        self._listeners: List[Callable[[str, AnalysisState], None]] = []

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
        # Notify listeners outside the lock to avoid deadlocks
        for listener in list(self._listeners):
            try:
                listener(analysis_id, new_state)
            except Exception:
                # Listener errors should not break orchestrator flow
                pass
        return record

    def list_records(self, limit: int) -> List[AnalysisRecord]:
        with self._lock:
            return list(self._store.values())[:limit]

    def subscribe(self, listener: Callable[[str, AnalysisState], None]) -> None:
        """Register a callback to receive state change events."""
        with self._lock:
            self._listeners.append(listener)

    def unsubscribe(self, listener: Callable[[str, AnalysisState], None]) -> None:
        """Remove a previously registered listener."""
        with self._lock:
            if listener in self._listeners:
                self._listeners.remove(listener)


# module-level orchestrator instance
orchestrator = Orchestrator()
