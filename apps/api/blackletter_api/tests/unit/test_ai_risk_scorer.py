from __future__ import annotations

import pytest

from blackletter_api.services.ai_risk_scorer import (
    AIRiskScorer,
    RiskCategory,
    RiskLevel,
)


def test_analyze_contract_risk_no_findings_returns_low_scores():
    """No findings and benign text should yield low risk across categories."""
    scorer = AIRiskScorer()
    contract_text = "Standard agreement with basic terms."

    profile = scorer.analyze_contract_risk(contract_text, [])

    factors = {f.category: f for f in profile.risk_factors}
    assert factors[RiskCategory.COMPLIANCE].level == RiskLevel.LOW
    assert factors[RiskCategory.FINANCIAL].level == RiskLevel.LOW
    assert factors[RiskCategory.OPERATIONAL].level == RiskLevel.LOW
    assert factors[RiskCategory.LEGAL].level == RiskLevel.LOW

    assert profile.overall_level == RiskLevel.LOW
    assert profile.overall_score == pytest.approx(0.1, abs=1e-6)


def test_analyze_contract_risk_weak_clauses_and_medium_other_risks():
    """Weak compliance clauses with financial and operational flags should produce medium overall risk."""
    scorer = AIRiskScorer()
    contract_text = (
        "The contract is valued at $5,000,000 with net 30 payment terms. "
        "It includes an SLA and dedicated staff."
    )
    findings = [{"verdict": "weak"}, {"verdict": "pass"}]

    profile = scorer.analyze_contract_risk(contract_text, findings)
    factors = {f.category: f for f in profile.risk_factors}

    assert factors[RiskCategory.COMPLIANCE].level == RiskLevel.HIGH
    assert factors[RiskCategory.FINANCIAL].level == RiskLevel.MEDIUM
    assert factors[RiskCategory.OPERATIONAL].level == RiskLevel.MEDIUM
    assert factors[RiskCategory.LEGAL].level == RiskLevel.LOW

    assert profile.overall_level == RiskLevel.MEDIUM
    assert profile.overall_score == pytest.approx(0.4725, abs=1e-4)


def test_analyze_contract_risk_critical_issues_drive_high_risk():
    """Multiple missing clauses and high-risk terms should yield a critical overall risk."""
    scorer = AIRiskScorer()
    contract_text = (
        "This contract is worth $10,000,000 with penalty clauses, net 30 payment terms, and an early termination fee. "
        "It requires an SLA, dedicated staff, and warns of vendor lock-in. "
        "A data breach or public announcement could lead to regulatory penalty. "
        "The governing law is New York with arbitration and a limitation of liability clause."
    )
    findings = [{"verdict": "missing"}, {"verdict": "missing"}]

    profile = scorer.analyze_contract_risk(contract_text, findings)
    factors = {f.category: f for f in profile.risk_factors}

    assert factors[RiskCategory.COMPLIANCE].level == RiskLevel.CRITICAL
    assert factors[RiskCategory.FINANCIAL].level == RiskLevel.HIGH
    assert factors[RiskCategory.OPERATIONAL].level == RiskLevel.HIGH
    assert factors[RiskCategory.LEGAL].level == RiskLevel.HIGH

    assert profile.overall_level == RiskLevel.CRITICAL
    assert profile.overall_score == pytest.approx(0.89, abs=1e-4)
