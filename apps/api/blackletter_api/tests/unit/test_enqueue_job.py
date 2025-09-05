from __future__ import annotations

import blackletter_api.services.tasks as tasks


def test_enqueue_job_sync(monkeypatch):
    called: dict[str, tuple] = {}

    def fake_process(job_id, analysis_id, filename, size):  # noqa: ANN001
        called["args"] = (job_id, analysis_id, filename, size)

    monkeypatch.setenv("JOB_SYNC", "1")
    monkeypatch.setattr(tasks, "process_job", fake_process)
    tasks.enqueue_job("jid", "aid", "file.pdf", 10)
    assert called["args"] == ("jid", "aid", "file.pdf", 10)


def test_enqueue_job_async(monkeypatch):
    called: dict[str, tuple] = {}

    def fake_delay(job_id, analysis_id, filename, size):  # noqa: ANN001
        called["args"] = (job_id, analysis_id, filename, size)

    monkeypatch.delenv("JOB_SYNC", raising=False)
    monkeypatch.setattr(tasks.process_job, "delay", fake_delay)
    tasks.enqueue_job("jid", "aid", "file.pdf", 5)
    assert called["args"] == ("jid", "aid", "file.pdf", 5)

