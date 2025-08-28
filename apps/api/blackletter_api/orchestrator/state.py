from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel


class AnalysisState(str, Enum):
    """Workflow states for an analysis job."""

    RECEIVED = "RECEIVED"
    EXTRACTED = "EXTRACTED"
    SEGMENTED = "SEGMENTED"
    GDPR_LEGAL_DONE = "GDPR_LEGAL_DONE"
    GC_DONE = "GC_DONE"
    REPORTED = "REPORTED"


class Analysis(BaseModel):
    id: str
    state: AnalysisState
    gdpr_done: bool = False
    legal_done: bool = False
    findings: Dict[str, List[dict]] = {}


class Orchestrator:
    """Simple in-memory orchestrator for the Stage-1 flow."""

    def __init__(self) -> None:
        self._analyses: Dict[str, Analysis] = {}

    def create(self) -> Analysis:
        analysis = Analysis(id=str(uuid4()), state=AnalysisState.RECEIVED)
        self._analyses[analysis.id] = analysis
        return analysis

    def get(self, analysis_id: str) -> Optional[Analysis]:
        return self._analyses.get(analysis_id)

    def handle_event(self, analysis_id: str, topic: str, payload: Optional[List[dict]] = None) -> Analysis:
        analysis = self._analyses[analysis_id]
        if topic == "document.extracted.v1":
            analysis.state = AnalysisState.EXTRACTED
        elif topic == "document.segmented.v1":
            analysis.state = AnalysisState.SEGMENTED
        elif topic == "gdpr.findings.ready.v1":
            analysis.gdpr_done = True
            analysis.findings["gdpr"] = payload or []
        elif topic == "legal.findings.ready.v1":
            analysis.legal_done = True
            analysis.findings["legal"] = payload or []
        elif topic == "gc.assessment.ready.v1":
            analysis.state = AnalysisState.GC_DONE
            analysis.findings["gc"] = payload or []
        elif topic == "report.published.v1":
            analysis.state = AnalysisState.REPORTED

        if analysis.state == AnalysisState.SEGMENTED and analysis.gdpr_done and analysis.legal_done:
            analysis.state = AnalysisState.GDPR_LEGAL_DONE

        self._analyses[analysis_id] = analysis
        return analysis


orchestrator = Orchestrator()
