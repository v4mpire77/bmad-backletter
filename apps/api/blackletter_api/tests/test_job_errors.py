from fastapi.testclient import TestClient

from apps.api.blackletter_api.main import app

client = TestClient(app)


def test_job_not_found_error():
    resp = client.get("/api/jobs/unknown")
    assert resp.status_code == 404
    assert resp.json() == {"code": "not_found", "detail": "Job not found"}
