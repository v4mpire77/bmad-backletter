from datetime import datetime

from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.services.ai_risk_scorer import ContractRiskProfile, RiskLevel


client = TestClient(app)


def test_risk_analysis_returns_iso_timestamp(monkeypatch) -> None:
    dummy_profile = ContractRiskProfile(
        overall_score=0.0,
        overall_level=RiskLevel.LOW,
        risk_factors=[],
        summary="",
        urgent_actions=[],
        monitoring_points=[],
    )

    def fake_analyze_contract_risk(contract_text: str, findings: list) -> ContractRiskProfile:
        return dummy_profile

    monkeypatch.setattr(
        "blackletter_api.routers.risk_analysis.ai_risk_scorer.analyze_contract_risk",
        fake_analyze_contract_risk,
    )

    res = client.post("/api/risk-analysis", json={"analysis_id": "test"})
    assert res.status_code == 200
    ts = res.json()["metadata"]["analysis_timestamp"]
    # ensure timestamp is valid ISO format
    datetime.fromisoformat(ts)
    assert "T" in ts
