from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def test_list_reports_initially_empty():
    res = client.get("/api/reports")
    assert res.status_code == 200
    assert res.json() == []


def test_create_report_and_list():
    payload = {"include_logo": True, "include_meta": False, "date_format": "MDY"}
    res = client.post("/api/reports/test123", json=payload)
    assert res.status_code == 201
    data = res.json()
    for key in ["id", "analysis_id", "filename", "created_at", "options"]:
        assert key in data
    assert data["analysis_id"] == "test123"
    # list reports now contains the created record
    res2 = client.get("/api/reports")
    assert res2.status_code == 200
    items = res2.json()
    assert any(r["id"] == data["id"] for r in items)
