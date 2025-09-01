import json
import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from backend.app.services.compliance_scanner import scan_document


def test_compliance_scan(tmp_path: Path):
    frameworks = {
        "gdpr": "rules/compliance/gdpr.json",
        "aml": "rules/compliance/aml_kyc.json",
        "uk_ics": "rules/compliance/uk_ics.json",
    }
    text = (
        "Our policy includes anti-money laundering and know your customer procedures "
        "to ensure safety for all parties."
    )
    report = scan_document(
        text, frameworks, user_id="user1", audit_path=str(tmp_path / "audit.log")
    )

    assert report.risk == "medium"
    assert len(report.frameworks) == 3
    gdpr_report = next(fr for fr in report.frameworks if fr.name == "gdpr")
    assert gdpr_report.score < 1
    assert any(v.rule_id == "gdpr-001" for v in gdpr_report.violations)

    log_file = tmp_path / "audit.log"
    assert log_file.exists()
    with open(log_file, "r", encoding="utf-8") as f:
        entry = json.loads(f.readline())
    assert entry["user_id"] == "user1"
    assert entry["risk"] == "medium"
