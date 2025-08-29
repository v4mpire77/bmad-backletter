from __future__ import annotations

import json
import uuid
from pathlib import Path

import pytest

from blackletter_api.services.token_ledger import (
    add_tokens,
    get_ledger,
    reset_ledger,
)
from blackletter_api.services.storage import analysis_dir


@pytest.fixture()
def analysis(tmp_path: Path, monkeypatch):
    analysis_id = str(uuid.uuid4())
    # Redirect analysis_dir to tmp
    monkeypatch.setattr(
        "blackletter_api.services.token_ledger.analysis_dir",
        lambda aid: tmp_path / aid,
    )
    return analysis_id


def test_off_by_one_cap(monkeypatch, analysis):
    monkeypatch.setenv("TOKEN_CAP_PER_DOC", "10")
    reset_ledger(analysis)
    # Add 9 tokens -> below cap
    add_tokens(analysis, 9)
    led = get_ledger(analysis)
    assert led.total_tokens == 9
    assert led.needs_review is False

    # Add 1 more -> equals cap triggers needs_review
    add_tokens(analysis, 1)
    led = get_ledger(analysis)
    assert led.total_tokens == 10
    assert led.needs_review is True


def test_provider_off_persists_zero_ledger(monkeypatch, analysis):
    monkeypatch.setenv("LLM_PROVIDER_ENABLED", "0")
    reset_ledger(analysis)

    # A zeroed ledger should be persisted
    led = get_ledger(analysis)
    base = analysis_dir(analysis)
    tokens_path = base / "tokens.json"
    assert tokens_path.exists()
    data = json.loads(tokens_path.read_text(encoding="utf-8"))
    assert data["total_tokens"] == 0
    assert data["needs_review"] is False


