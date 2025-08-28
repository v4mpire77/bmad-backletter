from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def test_intake_and_fetch_flow() -> None:
    res = client.post("/api/intake", json={"filename": "contract.pdf"})
    assert res.status_code == 200
    analysis_id = res.json()["analysis_id"]

    res = client.get(f"/api/analyses/{analysis_id}")
    assert res.status_code == 200
    summary = res.json()
    assert summary["id"] == analysis_id
    assert summary["state"] == "RECEIVED"

    res = client.get(f"/api/analyses/{analysis_id}/findings")
    assert res.status_code == 200
    assert res.json() == []

    res = client.get("/api/analyses?limit=10")
    assert res.status_code == 200
    data = res.json()
    assert any(item["id"] == analysis_id for item in data)
