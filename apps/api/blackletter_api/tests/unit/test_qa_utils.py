import pytest

from blackletter_api.services.document_qa import DocumentQAService
from blackletter_api.services.gemini_service import GeminiService


def test_extract_sources_orders_by_score_and_limits():
    service = DocumentQAService()
    chunks = [
        {"page": 1, "content": "a", "score": 0.1},
        {"page": 2, "content": "b", "score": 0.9},
        {"page": 3, "content": "c", "score": 0.5},
    ]
    sources = service._extract_sources(chunks, top_k=2)
    assert [s.page for s in sources] == [2, 3]
    assert [s.content for s in sources] == ["b", "c"]


def test_extract_sources_ignores_invalid_entries():
    service = DocumentQAService()
    chunks = [
        {"page": 1, "score": 0.3},  # missing content
        {"page": 2, "content": "ok", "score": 0.6},
    ]
    sources = service._extract_sources(chunks)
    assert len(sources) == 1
    assert sources[0].page == 2


def test_keyword_extraction_case_and_priority():
    service = GeminiService()
    text = (
        "WARNING: major ISSUE detected\n"
        "We recommend immediate action\n"
        "We recommend action to avoid risk\n"
        "Neutral line"
    )
    insights = service._extract_insights_from_text(text)
    assert insights["risk_factors"] == [
        "WARNING: major ISSUE detected",
        "We recommend action to avoid risk",
    ]
    assert insights["recommendations"] == ["We recommend immediate action"]


def test_keyword_extraction_no_keywords():
    service = GeminiService()
    text = "Just a neutral statement."
    insights = service._extract_insights_from_text(text)
    assert insights["risk_factors"] == []
    assert insights["recommendations"] == []
