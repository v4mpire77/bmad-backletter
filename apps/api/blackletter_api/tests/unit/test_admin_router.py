from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from blackletter_api.routers import admin


app = FastAPI()
app.include_router(admin.router)
client = TestClient(app)


class DummyMetricsService:
    def get_admin_metrics(self) -> dict[str, float | int]:
        return {
            "p95_latency_ms": 123.45,
            "avg_tokens_per_doc": 100,
            "llm_usage_percent": 50,
            "explainability_rate": 90,
            "total_analyses": 5,
            "hard_cap_limit": 1000,
            "cap_exceeded_count": 0,
        }

    def get_metrics_time_series(self, days: int) -> dict[str, list]:
        return {
            "dates": ["2024-01-01"],
            "tokens": [100],
            "llm_usage": [50],
            "latency": [123],
        }


class DummyLLMGate:
    hard_cap = 1000

    def get_current_token_usage(self, analysis_id: str) -> int:
        return 200

    def get_analysis_metrics(self) -> dict[str, int]:
        return {"avg_tokens_per_doc": 120}


def test_get_admin_metrics(monkeypatch) -> None:
    monkeypatch.setattr(
        "blackletter_api.routers.admin.get_metrics_service",
        lambda: DummyMetricsService(),
    )
    res = client.get("/api/admin/metrics")
    assert res.status_code == 200
    body = res.json()
    assert body["tiles"]["p95_latency"]["value"] == 123.45


def test_get_metrics_timeseries(monkeypatch) -> None:
    monkeypatch.setattr(
        "blackletter_api.routers.admin.get_metrics_service",
        lambda: DummyMetricsService(),
    )
    res = client.get("/api/admin/metrics/timeseries")
    assert res.status_code == 200
    body = res.json()
    assert body["timeseries"]["dates"] == ["2024-01-01"]


def test_get_analysis_token_usage(monkeypatch) -> None:
    monkeypatch.setattr(
        "blackletter_api.routers.admin.get_llm_gate",
        lambda: DummyLLMGate(),
    )
    res = client.get("/api/admin/token-usage/test-analysis")
    assert res.status_code == 200
    body = res.json()
    assert body["analysis_id"] == "test-analysis"


def test_get_aggregate_metrics(monkeypatch) -> None:
    monkeypatch.setattr(
        "blackletter_api.routers.admin.get_llm_gate",
        lambda: DummyLLMGate(),
    )
    res = client.get("/api/admin/metrics/aggregates")
    assert res.status_code == 200
    body = res.json()
    assert "aggregates" in body


def test_get_system_health(monkeypatch) -> None:
    monkeypatch.setattr(
        "blackletter_api.routers.admin.get_metrics_service",
        lambda: DummyMetricsService(),
    )
    monkeypatch.setattr(
        "blackletter_api.routers.admin.get_llm_gate",
        lambda: DummyLLMGate(),
    )
    res = client.get("/api/admin/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "healthy"

