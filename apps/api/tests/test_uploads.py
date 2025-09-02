import io
from fastapi.testclient import TestClient

from apps.api.main import app

client = TestClient(app)


def test_upload_success_and_job_status():
    data = io.BytesIO(b"hello")
    res = client.post(
        "/v1/docs/upload",
        files={"file": ("test.pdf", data, "application/pdf")},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "queued"
    job_id = body["job_id"]

    status_res = client.get(f"/v1/jobs/{job_id}")
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "queued"


def test_upload_invalid_type():
    data = io.BytesIO(b"bad")
    res = client.post(
        "/v1/docs/upload",
        files={"file": ("test.txt", data, "text/plain")},
    )
    assert res.status_code == 400
    assert "Unsupported" in res.json()["detail"]


def test_upload_too_large():
    data = io.BytesIO(b"a" * (10 * 1024 * 1024 + 1))
    res = client.post(
        "/v1/docs/upload",
        files={"file": ("big.pdf", data, "application/pdf")},
    )
    assert res.status_code == 400
    assert "too large" in res.json()["detail"].lower()


def test_upload_missing_file():
    res = client.post("/v1/docs/upload")
    assert res.status_code == 422


def test_job_not_found():
    res = client.get("/v1/jobs/unknown")
    assert res.status_code == 404
