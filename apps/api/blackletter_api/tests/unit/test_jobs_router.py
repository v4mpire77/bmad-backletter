from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def test_job_not_found():
    res = client.get("/api/jobs/missing")
    assert res.status_code == 404
    body = res.json()
    assert body["code"] == "not_found"
    assert isinstance(body["message"], str)
