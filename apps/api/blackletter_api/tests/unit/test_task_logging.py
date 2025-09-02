import logging

from apps.api.blackletter_api.services import tasks


def test_process_job_logs_error(monkeypatch, caplog):
    job_id = tasks.new_job(analysis_id="a1")

    def boom(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(tasks, "run_extraction", boom)

    with caplog.at_level(logging.INFO):
        tasks.process_job(job_id, "a1", "file.pdf", 0)

    record = next((r for r in caplog.records if r.msg == "task_error"), None)
    assert record is not None
    assert getattr(record, "job_id") == job_id
    assert getattr(record, "state") == "error"
