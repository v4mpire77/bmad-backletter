from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.orchestrator.state import orchestrator


client = TestClient(app)


def test_list_analyses_empty():
    orchestrator._store.clear()
    res = client.get("/api/analyses?limit=50")
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert body == []


def test_list_analyses_preserves_created_at():
    orchestrator._store.clear()
    analysis_id = orchestrator.intake("contract.pdf")
    created_at = orchestrator.summary(analysis_id).created_at.isoformat()
    res = client.get("/api/analyses?limit=50")
    assert res.status_code == 200
    body = res.json()
    assert body[0]["created_at"] == created_at


def test_analysis_summary_not_found():
    orchestrator._store.clear()
    res = client.get("/api/analyses/missing")
    assert res.status_code == 404
    body = res.json()
    assert body["code"] == "not_found"
    assert isinstance(body["message"], str)


def test_analysis_findings_not_found():
    orchestrator._store.clear()
    res = client.get("/api/analyses/missing/findings")
    assert res.status_code == 404
    body = res.json()
    assert body["code"] == "not_found"
    assert isinstance(body["message"], str)

