from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.orchestrator.state import orchestrator, AnalysisState


client = TestClient(app)


def test_list_analyses_empty():
    orchestrator._store.clear()
    res = client.get("/api/analyses?limit=50")
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert body == []


def test_analysis_summary_not_found():
    orchestrator._store.clear()
    res = client.get("/api/analyses/missing")
    assert res.status_code == 404
    body = res.json()
    assert body["code"] == "not_found"
    assert isinstance(body["message"], str)


def test_analysis_findings_include_fields():
    orchestrator._store.clear()
    analysis_id = orchestrator.intake("demo.pdf")
    orchestrator.advance(
        analysis_id,
        AnalysisState.REPORTED,
        finding={
            "detector_id": "D1",
            "verdict": "pass",
            "snippet": "text",
            "page": 1,
            "start": 0,
            "end": 4,
            "rationale": "reason",
        },
    )
    res = client.get(f"/api/analyses/{analysis_id}/findings")
    assert res.status_code == 200
    body = res.json()[0]
    assert body["rule_id"] == "D1"
    assert body["original_text"] == "text"
    assert body["suggested_text"] == "text"


def test_analysis_findings_not_found():
    orchestrator._store.clear()
    res = client.get("/api/analyses/missing/findings")
    assert res.status_code == 404
    body = res.json()
    assert body["code"] == "not_found"
    assert isinstance(body["message"], str)

