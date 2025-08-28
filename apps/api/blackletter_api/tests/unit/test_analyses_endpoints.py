from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.orchestrator.state import orchestrator

client = TestClient(app)


def test_intake_and_get_endpoints():
    orchestrator._analyses.clear()
    res = client.post("/api/intake")
    assert res.status_code == 200
    data = res.json()
    analysis_id = data["id"]
    assert data["state"] == "RECEIVED"

    res = client.get(f"/api/analyses/{analysis_id}")
    assert res.status_code == 200
    summary = res.json()
    assert summary["id"] == analysis_id
    assert summary["state"] == "RECEIVED"

    res = client.get(f"/api/analyses/{analysis_id}/findings")
    assert res.status_code == 200
    assert res.json() == {}
