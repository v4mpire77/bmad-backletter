import pathlib
import sys

import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from engine.gdpr import (Playbook, Rule, RuleOverride, RulesConfig,
                         analyze_document, segment_clauses)


def test_segment_clauses():
    text = "1. Intro\nHello\n2. Data\nStuff"
    clauses = segment_clauses(text)
    assert len(clauses) == 2
    assert clauses[0]["id"] == "1"
    assert clauses[1]["id"] == "2"


def test_analyze_document_and_vague_terms():
    rules_conf = RulesConfig(
        rules=[
            Rule(id="DATA", description="Data clause", primary_keywords=["data"]),
            Rule(id="BREACH", description="Breach", primary_keywords=["breach"]),
        ]
    )
    text = (
        "1. Data Protection\nThe processor shall protect personal data.\n"
        "2. Confidentiality\nEach party shall use reasonable efforts to keep secrets."
    )
    playbook = Playbook(enable_vague_terms_scan=True)
    issues = analyze_document("DOC1", text, rules_conf, playbook)
    statuses = {
        issue.rule_id: issue.status for issue in issues if issue.rule_id != "VAGUE_TERM"
    }
    assert statuses["DATA"] == "found"
    assert statuses["BREACH"] == "missing"
    assert any(issue.rule_id == "VAGUE_TERM" for issue in issues)


def test_playbook_override_disables_rule():
    rules_conf = RulesConfig(
        rules=[Rule(id="DATA", description="Data clause", primary_keywords=["data"])]
    )
    playbook = Playbook(rules={"DATA": RuleOverride(enabled=False)})
    issues = analyze_document("DOC2", "1. Data\ntext", rules_conf, playbook)
    assert issues == []
