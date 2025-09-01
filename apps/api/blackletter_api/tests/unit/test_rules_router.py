from __future__ import annotations

from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.services.rulepack_loader import RulepackError


client = TestClient(app)


def test_rules_summary_handles_loader_error(monkeypatch) -> None:
    def _raise(*args, **kwargs):  # type: ignore[unused-arg]
        raise RulepackError("boom")

    monkeypatch.setattr("blackletter_api.routers.rules.load_rulepack", _raise)
    res = client.get("/api/rules/summary")
    assert res.status_code == 500
    assert res.json()["detail"] == "Rulepack error: boom"
