import time
from io import BytesIO

import fakeredis
from fastapi.testclient import TestClient

from blackletter_api.main import app
import blackletter_api.services.tasks as tasks


client = TestClient(app)


def _post_upload_ok():
    files = {"file": ("doc.pdf", BytesIO(b"%PDF-1.4 minimal"), "application/pdf")}
    return client.post("/api/contracts", files=files)


def test_job_polling_async_success(monkeypatch):
    tasks.celery_app.conf.task_always_eager = True
    tasks.celery_app.conf.task_eager_propagates = True
    monkeypatch.setattr(tasks, "redis_client", fakeredis.FakeRedis(decode_responses=True))

    resp = _post_upload_ok()
    assert resp.status_code == 201, resp.text
    data = resp.json()
    job_id = data["id"]
    analysis_id = data["analysis_id"]

    # Poll until job leaves 'queued' state or timeout
    status = data["status"]
    deadline = time.time() + 2.0
    while status == "queued" and time.time() < deadline:
        s = client.get(f"/api/jobs/{job_id}")
        assert s.status_code == 200
        status = s.json()["status"]
        time.sleep(0.02)

    assert status in ("running", "done")

    # extraction.json should exist
    from pathlib import Path

    extraction_path = Path('.data') / 'analyses' / analysis_id / 'extraction.json'
    assert extraction_path.exists(), f"missing {extraction_path}"


def test_job_polling_error(monkeypatch):
    # Force synchronous execution and simulate extraction failure
    tasks.celery_app.conf.task_always_eager = True
    tasks.celery_app.conf.task_eager_propagates = True
    monkeypatch.setattr(tasks, "redis_client", fakeredis.FakeRedis(decode_responses=True))

    def boom(*args, **kwargs):  # noqa: ANN001
        raise RuntimeError("boom")

    monkeypatch.setattr(tasks, "run_extraction", boom)

    resp = _post_upload_ok()
    assert resp.status_code == 201, resp.text
    job_id = resp.json()["id"]

    # Poll for error state (should be immediate in sync mode)
    s = client.get(f"/api/jobs/{job_id}")
    assert s.status_code == 200
    sd = s.json()
    assert sd["status"] == "error"
    assert "error_reason" in sd or "error" in sd
