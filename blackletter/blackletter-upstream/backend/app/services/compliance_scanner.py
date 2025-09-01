from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from ..models import rules as m
from .rules_validator import load_rules


@dataclass
class RuleViolation:
    """Represents a single rule violation."""

    rule_id: str
    severity: m.Severity
    message: str | None
    remediation: str | None


@dataclass
class FrameworkReport:
    """Report for a single compliance framework."""

    name: str
    score: float
    violations: List[RuleViolation]


@dataclass
class ComplianceReport:
    """Aggregated compliance report for a document."""

    user_id: str
    timestamp: datetime
    overall_score: float
    risk: str
    frameworks: List[FrameworkReport]


def _evaluate_rule(rule: m.Rule, text: str) -> bool:
    """Evaluate a rule against document text."""

    for check in rule.checks:
        if isinstance(check, m.RegexAnyCheck):
            hits = sum(1 for p in check.patterns if re.search(p, text, re.IGNORECASE))
            if hits < (check.min_hits or 1):
                return False
        elif isinstance(check, m.RegexAllCheck):
            for p in check.patterns:
                if not re.search(p, text, re.IGNORECASE):
                    return False
        elif isinstance(check, m.NegationRegexCheck):
            matched = bool(re.search(check.pattern, text, re.IGNORECASE))
            if check.must_not_match and matched:
                return False
            if not check.must_not_match and not matched:
                return False
        # Other check types are ignored for now
    return True


def _framework_score(ruleset: m.RuleSet, text: str) -> FrameworkReport:
    violations: List[RuleViolation] = []
    weights = ruleset.meta.scoring.weights
    total = 0
    failed = 0
    for rule in ruleset.rules:
        passed = _evaluate_rule(rule, text)
        weight = weights[rule.severity]
        total += weight
        if not passed:
            failed += weight
            msg = rule.messages.fail if rule.messages else None
            violations.append(
                RuleViolation(
                    rule_id=rule.id,
                    severity=rule.severity,
                    message=msg,
                    remediation=rule.remediation,
                )
            )
    score = (total - failed) / total if total else 1.0
    return FrameworkReport(
        name="".join(ruleset.jurisdiction), score=score, violations=violations
    )


def _risk(score: float) -> str:
    if score >= 0.8:
        return "low"
    if score >= 0.5:
        return "medium"
    return "high"


def generate_report(report: ComplianceReport) -> Dict:
    """Convert a ComplianceReport to serialisable dict."""

    return {
        "user_id": report.user_id,
        "timestamp": report.timestamp.isoformat(),
        "overall_score": report.overall_score,
        "risk": report.risk,
        "frameworks": [
            {
                "name": fr.name,
                "score": fr.score,
                "violations": [
                    {
                        "rule_id": v.rule_id,
                        "severity": v.severity,
                        "message": v.message,
                        "remediation": v.remediation,
                    }
                    for v in fr.violations
                ],
            }
            for fr in report.frameworks
        ],
    }


def _log_audit(report: ComplianceReport, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(generate_report(report)) + "\n")


def scan_document(
    text: str,
    frameworks: Dict[str, str],
    user_id: str,
    audit_path: str | None = None,
) -> ComplianceReport:
    """Scan document text against multiple compliance frameworks.

    Args:
        text: Document content.
        frameworks: Mapping of framework name to rules path.
        user_id: ID of the user initiating the scan.
        audit_path: Optional path to audit log file.

    Returns:
        ComplianceReport with scores and violations.
    """

    reports: List[FrameworkReport] = []
    for name, path in frameworks.items():
        ruleset = load_rules(path)
        fr = _framework_score(ruleset, text)
        fr.name = name
        reports.append(fr)

    overall = sum(fr.score for fr in reports) / len(reports) if reports else 1.0
    report = ComplianceReport(
        user_id=user_id,
        timestamp=datetime.utcnow(),
        overall_score=overall,
        risk=_risk(overall),
        frameworks=reports,
    )

    audit_file = audit_path or os.path.join("logs", "compliance_audit.log")
    _log_audit(report, audit_file)
    return report
