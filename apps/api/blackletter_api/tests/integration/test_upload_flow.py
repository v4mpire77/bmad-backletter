from __future__ import annotations

from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def test_post_upload_creates_job_and_get_status():
    files = {"file": ("sample.txt", b"dummy content", "text/plain")}
    resp = client.post("/api/uploads", files=files)
    assert resp.status_code == 200
    data = resp.json()
    assert "job_id" in data and isinstance(data["job_id"], str)

    job_id = data["job_id"]
    status_resp = client.get(f"/api/jobs/{job_id}")
    assert status_resp.status_code == 200
    job = status_resp.json()
    assert job["id"] == job_id
    assert job["state"] in {"queued", "processing", "completed"}
    assert job["rulepack_version"]

