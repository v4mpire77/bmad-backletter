import json

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from blackletter_api.services.evidence import build_window, handle_boundary_cases
from blackletter_api.models.entities import Base, OrgSetting, LLMProvider, RetentionPolicy


SAMPLE_DATA = {
    "page_map": [
        {"page": 1, "start": 0, "end": 202},
        {"page": 2, "start": 202, "end": 222},
    ],
    "sentences": [
        {"page": 1, "start": 0, "end": 25, "text": "This is the first sentence."},
        {"page": 1, "start": 26, "end": 55, "text": "This is the second sentence."},
        {"page": 1, "start": 56, "end": 83, "text": "This is the third sentence."},
        {"page": 1, "start": 84, "end": 113, "text": "This is the fourth sentence."},
        {"page": 1, "start": 114, "end": 142, "text": "This is the fifth sentence."},
        {"page": 1, "start": 143, "end": 171, "text": "This is the sixth sentence."},
        {"page": 1, "start": 172, "end": 201, "text": "This is the seventh sentence."},
        {"page": 2, "start": 0, "end": 20, "text": "A sentence on page 2."},
    ],
}


@pytest.fixture
def analysis(tmp_path, monkeypatch) -> str:
    """Create a temporary analysis directory with sentence metadata."""

    analysis_id = "analysis123"
    base = tmp_path / analysis_id
    base.mkdir()

    monkeypatch.setattr(
        "blackletter_api.services.evidence.analysis_dir", lambda aid: base
    )
    (base / "sentences.json").write_text(json.dumps(SAMPLE_DATA), encoding="utf-8")
    return analysis_id


def test_build_window_standard_case(analysis: str) -> None:
    result = build_window(analysis, 90, 94)

    assert result["page"] == 1
    assert result["start"] == 26
    assert result["end"] == 171
    assert (
        result["snippet"]
        == "This is the second sentence. This is the third sentence. This is the fourth sentence. This is the fifth sentence. This is the sixth sentence."
    )


def test_build_window_start_edge_case(analysis: str) -> None:
    result = build_window(analysis, 5, 10)

    assert result["page"] == 1
    assert result["start"] == 0
    assert result["end"] == 83
    assert (
        result["snippet"]
        == "This is the first sentence. This is the second sentence. This is the third sentence."
    )


def test_build_window_end_edge_case(analysis: str) -> None:
    result = build_window(analysis, 180, 185)

    assert result["page"] == 1
    assert result["start"] == 114
    assert result["end"] == 201
    assert (
        result["snippet"]
        == "This is the fifth sentence. This is the sixth sentence. This is the seventh sentence."
    )


def test_build_window_custom_size(analysis: str) -> None:
    result = build_window(analysis, 90, 94, n_sentences=1)

    assert result["page"] == 1
    assert result["start"] == 56
    assert result["end"] == 142
    assert (
        result["snippet"]
        == "This is the third sentence. This is the fourth sentence. This is the fifth sentence."
    )


def test_build_window_cross_page_span(analysis: str) -> None:
    """Span crosses page boundary but window remains on start page."""

    result = build_window(analysis, 190, 210)

    assert result["page"] == 1
    assert result["start"] == 114
    assert result["end"] == 201
    assert "page 2" not in result["snippet"]


def test_build_window_no_page_leakage(analysis: str) -> None:
    start = 202 + 5
    end = 202 + 10
    result = build_window(analysis, start, end)

    assert result["page"] == 2
    assert result["start"] == 202
    assert result["end"] == 222
    assert result["snippet"] == "A sentence on page 2."


@pytest.fixture
def session_factory():
    def _factory(n_sentences: int):
        engine = create_engine(
            "sqlite:///:memory:", connect_args={"check_same_thread": False}
        )
        TestingSession = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        session = TestingSession()
        setting = OrgSetting(
            llm_provider=LLMProvider.none,
            ocr_enabled=False,
            retention_policy=RetentionPolicy.none,
            evidence_window_sentences=n_sentences,
        )
        session.add(setting)
        session.commit()
        return session

    return _factory


def test_build_window_uses_org_setting_contracts(analysis: str, session_factory) -> None:
    db = session_factory(1)
    result = build_window(analysis, 90, 94, db=db)

    assert result["start"] == 56
    assert result["end"] == 142
    assert (
        result["snippet"]
        == "This is the third sentence. This is the fourth sentence. This is the fifth sentence."
    )
    db.close()


def test_build_window_uses_org_setting_expands(analysis: str, session_factory) -> None:
    db = session_factory(3)
    result = build_window(analysis, 90, 94, db=db)

    assert result["start"] == 0
    assert result["end"] == 201
    assert (
        result["snippet"]
        == "This is the first sentence. This is the second sentence. This is the third sentence. This is the fourth sentence. This is the fifth sentence. This is the sixth sentence. This is the seventh sentence."
    )
    db.close()


def test_handle_boundary_cases_start_of_document() -> None:
    text = "This is a test document with multiple sentences. " * 10
    result = handle_boundary_cases(text, 5, 15, 2)

    assert result["start"] == 0
    assert result["boundary_adjusted"] is True
    assert "snippet" in result


def test_handle_boundary_cases_end_of_document() -> None:
    text = "Short text."
    result = handle_boundary_cases(text, 8, 10, 2)

    assert result["end"] == len(text)
    assert result["boundary_adjusted"] is True


def test_handle_boundary_cases_non_ascii() -> None:
    text = "This has émojis 🎉 and unicode ñ characters."
    result = handle_boundary_cases(text, 10, 20, 2)

    assert "snippet" in result
    assert len(result["snippet"]) > 0

