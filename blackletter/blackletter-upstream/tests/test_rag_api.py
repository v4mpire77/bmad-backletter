"""Tests for the small FastAPI surface in ``rag.api``."""

import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from rag.api import app  # noqa: E402

client = TestClient(app)


def test_batch_qa_returns_responses():
    payload = {
        "questions": [
            {"question": "One?"},
            {"question": "Two?"},
        ]
    }
    res = client.post("/rag/batch-qa", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["responses"]) == 2


def test_export_passes_filters(monkeypatch):
    called = {}

    def fake_retrieve(query, *, contract_id=None, ruleset=None, severity=None, **_):
        called["args"] = {
            "query": query,
            "contract_id": contract_id,
            "ruleset": ruleset,
            "severity": severity,
        }
        return {"query": query, "results": [{"a": 1}]}

    monkeypatch.setattr("rag.api.retrieve", fake_retrieve)
    payload = {
        "question": "Q?",
        "contract_id": "c1",
        "ruleset": "r1",
        "severity": "high",
    }
    res = client.post("/rag/export?format=json", json=payload)
    assert res.status_code == 200
    assert called["args"] == {
        "query": "Q?",
        "contract_id": "c1",
        "ruleset": "r1",
        "severity": "high",
    }


def test_analytics_counts_increment():
    # Trigger a QA call and an export call to generate analytics
    client.post("/rag/qa", json={"question": "Q"})
    client.post("/rag/export", json={"question": "Q"})
    res = client.get("/rag/analytics")
    data = res.json()
    assert data["qa"] >= 1
    assert data["export"] >= 1
