from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def test_list_analyses_stub():
    res = client.get("/api/analyses?limit=50")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)


def test_get_analysis_summary_stub():
    res = client.get("/api/analyses/abc123")
    assert res.status_code == 200
    data = res.json()
    # shape assertions
    for key in ["id", "filename", "created_at", "size", "verdicts"]:
        assert key in data
    assert data["id"] == "abc123"
    v = data["verdicts"]
    for k in ["pass_count", "weak_count", "missing_count", "needs_review_count"]:
        assert k in v


def test_get_analysis_findings_stub():
    res = client.get("/api/analyses/abc123/findings")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)

