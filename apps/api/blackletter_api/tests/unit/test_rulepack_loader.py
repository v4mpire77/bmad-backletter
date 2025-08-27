from __future__ import annotations

import os
from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

# Ensure `apps/api` is on sys.path so `blackletter_api` can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from blackletter_api.main import app  # type: ignore
from blackletter_api.services.rulepack_loader import (  # type: ignore
    RulepackError,
    RulepackLoader,
)


def write_file(p: Path, content: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def test_loader_happy_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
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


def test_loader_invalid_missing_detectors(tmp_path: Path):
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


def test_api_rules_summary(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
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
terms:
  - could
  - might
        """.strip(),
    )

    # Configure env for default loader used by router
    monkeypatch.setenv("RULES_DIR", str(rules_dir))
    monkeypatch.setenv("RULEPACK_FILE", "pack.yaml")
    monkeypatch.setenv("APP_ENV", "dev")

    client = TestClient(app)
    resp = client.get("/api/rules/summary")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["name"] == "art28"
    assert data["detector_count"] == 1
    assert data["lexicons"] == ["weak_language"]
