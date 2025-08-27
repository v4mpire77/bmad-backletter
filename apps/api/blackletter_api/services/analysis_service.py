from __future__ import annotations

from typing import Protocol

from blackletter_api.models.analysis import (
    AnalysisDetail,
    AnalysisListFilters,
    AnalysisListResponse,
)


class AnalysisRepository(Protocol):
    """Protocol for repositories that can be used by the service layer."""

    def list(self, filters: AnalysisListFilters) -> AnalysisListResponse:
        ...

    def get(self, analysis_id: str) -> AnalysisDetail:
        ...


class AnalysisService:
    """
    Orchestrates analysis listing and retrieval.

    This service is intentionally thin for now; the implementation will be
    provided later and can target any `AnalysisRepository` implementation
    (in-memory, SQL, etc.).
    """

    def __init__(self, repo: AnalysisRepository):
        self.repo = repo

    def list_analyses(self, filters: AnalysisListFilters) -> AnalysisListResponse:
        return self.repo.list(filters)

    def get_analysis(self, analysis_id: str) -> AnalysisDetail:
        return self.repo.get(analysis_id)

