from __future__ import annotations

import os
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Ensure `apps/api` is on sys.path so `blackletter_api` can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from blackletter_api.models.schemas import RulesSummary  # type: ignore
from blackletter_api.routers.rules import router as rules_router  # type: ignore


def write_file(p: Path, content: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def test_loader_happy_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from blackletter_api.services.rulepack_loader import (  # type: ignore
        RulepackError,
        RulepackLoader,
    )

    rules_dir = tmp_path / "rules"
    lex_dir = rules_dir / "lexicons"
    write_file(
        rules_dir / "pack.yaml",
        """
name: art28
version: v1
detectors:
  - id: weak_language
    type: lexicon
    description: Flags weak words
    lexicon: weak_language.yaml
lexicons:
  - file: weak_language.yaml
        """.strip(),
    )
    write_file(
        lex_dir / "weak_language.yaml",
        """
name: weak_language
terms:
  - may
  - should
  - attempt
        """.strip(),
    )

    loader = RulepackLoader(rules_dir, rulepack_file="pack.yaml", app_env="dev")
    rp = loader.load()
    assert rp.name == "art28"
    assert rp.version == "v1"
    assert len(rp.detectors) == 1
    assert "weak_language" in rp.lexicons
    assert "may" in rp.lexicons["weak_language"].terms


def test_loader_invalid_missing_detectors(tmp_path: Path) -> None:
    from blackletter_api.services.rulepack_loader import (  # type: ignore
        RulepackError,
        RulepackLoader,
    )

    rules_dir = tmp_path / "rules"
    write_file(
        rules_dir / "pack.yaml",
        """
name: art28
version: v1
        """.strip(),
    )

    loader = RulepackLoader(rules_dir, rulepack_file="pack.yaml", app_env="dev")
    with pytest.raises(RulepackError):
        loader.load()


def test_api_rules_summary(monkeypatch: pytest.MonkeyPatch) -> None:
    dummy_rp = SimpleNamespace(
        name="art28",
        version="v1",
        detectors=[
            SimpleNamespace(
                id="weak_language",
                type="lexicon",
                description="Flags weak words",
                lexicon="weak_language",
            )
        ],
        lexicons={"weak_language": object()},
    )
    monkeypatch.setattr(
        "blackletter_api.routers.rules.load_rulepack", lambda: dummy_rp
    )

    app = FastAPI()
    app.include_router(rules_router, prefix="/api")
    client = TestClient(app)
    resp = client.get("/api/rules/summary")
    assert resp.status_code == 200, resp.text
    data = RulesSummary(**resp.json())
    assert data.name == "art28"
    assert data.detector_count == 1
    assert data.lexicons == ["weak_language"]
