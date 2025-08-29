import json
import os
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.services.storage import analysis_dir


client = TestClient(app)


def _write_dummy_extraction(analysis_id: str, tokens_target: int) -> Path:
    base = analysis_dir(analysis_id)
    # Create a long text to approximate tokens when provider enabled
    text = "x" * (tokens_target * 4)
    sentences = [{"page": 1, "start": 0, "end": len(text), "text": text + " may"}]
    payload = {"text_path": "extracted.txt", "page_map": [{"page": 1, "start": 0, "end": len(text)}], "sentences": sentences}
    p = base / "extraction.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return p


@pytest.fixture(autouse=True)
def _env_caps(monkeypatch):
    monkeypatch.setenv("JOB_SYNC", "1")
    monkeypatch.setenv("LLM_PROVIDER_ENABLED", "1")
    monkeypatch.setenv("TOKEN_CAP_PER_DOC", "100")
    yield


def test_token_caps_enforced_and_metrics_exposed(monkeypatch):
    # Create analysis directory and dummy extraction large enough to exceed cap
    analysis_id = str(uuid.uuid4())
    base = analysis_dir(analysis_id)
    base.mkdir(parents=True, exist_ok=True)
    _write_dummy_extraction(analysis_id, tokens_target=150)  # > cap

    # Run detector runner directly to accrue tokens and trigger cap
    from blackletter_api.services.detector_runner import run_detectors
    run_detectors(analysis_id, str(base / "extraction.json"))

    # Verify tokens.json indicates needs_review
    tokens_path = base / "tokens.json"
    assert tokens_path.exists()
    data = json.loads(tokens_path.read_text(encoding="utf-8"))
    assert data["total_tokens"] >= 100
    assert data["needs_review"] is True
    assert "token_cap_exceeded" in (data.get("reason") or "")

    # Call metrics endpoint
    res = client.get("/api/admin/metrics")
    assert res.status_code == 200
    body = res.json()
    items = body.get("tokens_per_doc", [])
    assert any(it["analysis_id"] == analysis_id and it["needs_review"] for it in items)

