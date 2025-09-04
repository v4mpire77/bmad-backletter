from datetime import datetime, timezone
from pydantic import BaseModel

from blackletter_api.routers.findings import get_findings
from blackletter_api.services.tasks import JobRecord, JobState


def test_findings_endpoint_returns_required_fields(monkeypatch) -> None:
    job_id = "job123"
    job = JobRecord(
        id=job_id,
        status=JobState.done,
        analysis_id="analysis123",
        error_reason=None,
        created_at=datetime.now(timezone.utc),
    )
    monkeypatch.setattr("blackletter_api.routers.findings.get_job", lambda _: job)

    sample_findings = [
        {"original_text": "alpha", "suggested_text": "beta", "rule_id": "R1"},
        {"original_text": "gamma", "suggested_text": "delta", "rule_id": "R2"},
    ]
    monkeypatch.setattr(
        "blackletter_api.routers.findings.storage.get_analysis_findings",
        lambda _aid: sample_findings,
    )

    class FakeFinding(BaseModel):
        original_text: str
        suggested_text: str
        rule_id: str

    monkeypatch.setattr("blackletter_api.routers.findings.Finding", FakeFinding)

    findings = get_findings(job_id=job_id)
    assert isinstance(findings, list)
    for f in findings:
        data = f.model_dump()
        assert "original_text" in data
        assert "suggested_text" in data
        assert "rule_id" in data
