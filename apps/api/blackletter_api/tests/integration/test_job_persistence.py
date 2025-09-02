from io import BytesIO
from fastapi.testclient import TestClient

from blackletter_api.main import app
import blackletter_api.services.tasks as tasks


def test_job_persists_across_restarts(monkeypatch):
    monkeypatch.setattr(tasks.process_job, "delay", lambda *a, **k: None)
    client = TestClient(app)
    files = {"file": ("doc.pdf", BytesIO(b"data"), "application/pdf")}
    resp = client.post("/api/contracts", files=files)
    assert resp.status_code == 201
    job_id = resp.json()["id"]
    client.close()

    new_client = TestClient(app)
    status = new_client.get(f"/api/jobs/{job_id}")
    assert status.status_code == 200
    data = status.json()
    assert data["id"] == job_id
    assert data["status"] == "queued"
