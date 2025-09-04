from fastapi import APIRouter
from fastapi.testclient import TestClient
import pytest

from blackletter_api.routers import rules, admin

# Ensure main app imports even if some routers are placeholders
rules.router = APIRouter()
from blackletter_api.main import app

client = TestClient(app)


def test_metrics_schema():
    resp = client.get("/api/admin/metrics")
    assert resp.status_code == 200
    data = resp.json()
    for key in ["p95_latency", "tokens_per_doc", "llm_usage", "explainability_rate"]:
        assert set(data["tiles"][key]) == {"value", "unit", "label", "status"}
    assert set(data["summary"]) == {"total_analyses", "hard_cap_limit", "cap_exceeded_count"}


def test_metrics_error(monkeypatch):
    def boom():
        raise Exception("boom")

    monkeypatch.setattr(admin, "get_metrics_service", boom)
    resp = client.get("/api/admin/metrics")
    assert resp.status_code == 500
    assert resp.json()["detail"].startswith("Failed to retrieve admin metrics")


def test_metrics_timeseries_schema():
    resp = client.get("/api/admin/metrics/timeseries?days=1")
    assert resp.status_code == 200
    data = resp.json()
    assert set(data["timeseries"]) == {"dates", "tokens", "llm_usage", "latency"}
    meta = data["metadata"]
    assert meta["days_requested"] == 1
    assert meta["data_points"] == len(data["timeseries"]["dates"])
    assert "last_updated" in meta


def test_metrics_timeseries_error(monkeypatch):
    def boom():
        raise Exception("boom")

    monkeypatch.setattr(admin, "get_metrics_service", boom)
    resp = client.get("/api/admin/metrics/timeseries")
    assert resp.status_code == 500
    assert resp.json()["detail"].startswith("Failed to retrieve time series data")


def test_token_usage_schema():
    resp = client.get("/api/admin/token-usage/test")
    assert resp.status_code == 200
    data = resp.json()
    assert data["analysis_id"] == "test"
    assert {"tokens_per_doc", "hard_cap_limit", "cap_exceeded", "usage_percentage"} <= data.keys()


def test_token_usage_error(monkeypatch):
    def boom():
        raise Exception("boom")

    monkeypatch.setattr(admin, "get_llm_gate", boom)
    resp = client.get("/api/admin/token-usage/test")
    assert resp.status_code == 500
    assert resp.json()["detail"].startswith("Failed to retrieve token usage")


def test_metrics_aggregates_schema(monkeypatch):
    class DummyGate:
        def get_analysis_metrics(self):
            return {
                "avg_tokens_per_doc": 0.0,
                "percent_docs_invoking_llm": 0.0,
                "total_analyses": 0,
                "total_tokens": 0,
                "cap_exceeded_count": 0,
                "hard_cap_limit": 1000,
            }

    monkeypatch.setattr(admin, "get_llm_gate", lambda: DummyGate())

    resp = client.get("/api/admin/metrics/aggregates")
    assert resp.status_code == 200
    data = resp.json()
    agg = data["aggregates"]
    expected = {
        "avg_tokens_per_doc",
        "percent_docs_invoking_llm",
        "total_analyses",
        "total_tokens",
        "cap_exceeded_count",
        "hard_cap_limit",
    }
    assert expected <= agg.keys()
    assert data["computed_at"] == "recent"
    assert data["scope"] == "last_30_runs"


def test_metrics_aggregates_error(monkeypatch):
    def boom():
        raise Exception("boom")

    monkeypatch.setattr(admin, "get_llm_gate", boom)
    resp = client.get("/api/admin/metrics/aggregates")
    assert resp.status_code == 500
    assert resp.json()["detail"].startswith("Failed to retrieve aggregate metrics")

