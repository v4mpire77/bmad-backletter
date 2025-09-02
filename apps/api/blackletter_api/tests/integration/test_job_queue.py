import fakeredis
from io import BytesIO
from fastapi.testclient import TestClient

from blackletter_api.main import app
import blackletter_api.services.tasks as tasks

client = TestClient(app)


def test_upload_enqueues_job(monkeypatch):
    called = {}

    def fake_delay(job_id, analysis_id, filename, size):
        called["args"] = (job_id, analysis_id, filename, size)

    monkeypatch.setattr(tasks.process_job, "delay", fake_delay)

    files = {"file": ("doc.pdf", BytesIO(b"data"), "application/pdf")}
    resp = client.post("/api/contracts", files=files)
    assert resp.status_code == 201, resp.text
    assert "args" in called
    job_id, analysis_id, filename, size = called["args"]
    data = resp.json()
    assert job_id == data["id"]
    assert analysis_id == data["analysis_id"]
    assert filename.endswith(".pdf")
