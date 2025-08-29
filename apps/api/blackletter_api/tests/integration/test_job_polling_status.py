from __future__ import annotations

import time
from io import BytesIO

from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def _post_upload_ok():
    files = {"file": ("doc.pdf", BytesIO(b"%PDF-1.4 minimal"), "application/pdf")}
    return client.post("/api/contracts", files=files)


def test_job_polling_async_success(monkeypatch):
    # Ensure async background task mode by unsetting JOB_SYNC
    monkeypatch.delenv("JOB_SYNC", raising=False)

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

    # In minimal PDF bytes case, backend may error when opening.
    assert status in ("running", "done", "error")

    # extraction.json should exist
    from pathlib import Path

    extraction_path = Path('.data') / 'analyses' / analysis_id / 'extraction.json'
    assert extraction_path.exists(), f"missing {extraction_path}"


def test_job_polling_error(monkeypatch):
    # Force synchronous execution and simulate extraction failure
    monkeypatch.setenv("JOB_SYNC", "1")

    def boom(*args, **kwargs):  # noqa: ANN001
        raise RuntimeError("boom")

    import blackletter_api.services.tasks as tasks
    # Patch the symbol used inside process_job
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
