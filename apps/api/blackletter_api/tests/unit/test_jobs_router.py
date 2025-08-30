from __future__ import annotations

from datetime import datetime, timezone

from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.services.tasks import JobRecord, JobState

client = TestClient(app)


def test_get_job_status_returns_record(monkeypatch) -> None:
    record = JobRecord(
        id="job1",
        status=JobState.done,
        analysis_id="a1",
        error_reason=None,
        created_at=datetime.now(timezone.utc),
    )
    monkeypatch.setattr("blackletter_api.routers.jobs.get_job", lambda job_id: record)
    resp = client.get("/api/jobs/job1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "done"
    assert data["analysis_id"] == "a1"


def test_get_job_status_not_found(monkeypatch) -> None:
    monkeypatch.setattr("blackletter_api.routers.jobs.get_job", lambda job_id: None)
    resp = client.get("/api/jobs/missing")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "not_found"}
