from __future__ import annotations

from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def test_metrics_endpoint_structure():
    resp = client.get("/api/metrics")
    assert resp.status_code == 200
    data = resp.json()
    assert "counts" in data and isinstance(data["counts"], dict)
    assert "total_jobs" in data and isinstance(data["total_jobs"], int)
    assert "average_processing_seconds" in data

