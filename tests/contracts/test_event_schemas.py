import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")
validate = jsonschema.validate
ValidationError = jsonschema.ValidationError

BASE = Path(__file__).resolve().parents[2]
SCHEMA_DIR = BASE / "contracts" / "events"


def load_schema(name: str):
    with open(SCHEMA_DIR / name) as f:
        return json.load(f)


def sample_event(topic: str):
    meta = {
        "message_id": "1",
        "analysis_id": "A1",
        "correlation_id": "C1",
        "producer": "tester",
        "ts": "2024-01-01T00:00:00Z",
        "topic": topic,
        "schema": f"{topic}.schema.json",
    }
    base = {"meta": meta}
    if topic == "client.contract.received.v1":
        base["payload"] = {"file_url": "http://example.com/doc.pdf"}
    elif topic == "document.extracted.v1":
        base["payload"] = {
            "text": "hello",
            "sentences": [{"id": "s1", "text": "hello", "start_offset": 0, "end_offset": 5}],
            "page_map": [{"page": 1, "start_offset": 0, "end_offset": 5}],
        }
    elif topic == "document.segmented.v1":
        base["payload"] = {
            "clauses": [{"id": "c1", "type": "security", "start_offset": 0, "end_offset": 5}],
            "anchors": ["security"],
        }
    elif topic == "gdpr.findings.ready.v1":
        base["payload"] = {
            "findings": [
                {
                    "id": "f1",
                    "rule_id": "a",
                    "verdict": "Pass",
                    "snippet": "sample",
                    "start_offset": 0,
                    "end_offset": 6,
                    "rationale": "text",
                }
            ]
        }
    elif topic == "legal.findings.ready.v1":
        base["payload"] = {
            "findings": [
                {
                    "id": "l1",
                    "rule_id": "CONF-001",
                    "verdict": "Weak",
                    "snippet": "sample",
                    "start_offset": 0,
                    "end_offset": 6,
                    "rationale": "text",
                }
            ]
        }
    elif topic == "gc.assessment.ready.v1":
        base["payload"] = {
            "risk": {
                "level": "Low",
                "actions": [{"id": "a1", "finding_id": "f1", "description": "do"}],
            }
        }
    elif topic == "report.published.v1":
        base["payload"] = {"report_url": "http://example.com/report.pdf"}
    else:
        base["payload"] = {}
    return base


def test_envelope_schema():
    schema = load_schema("envelope.schema.json")
    event = sample_event("client.contract.received.v1")
    validate(event, schema)


def test_gdpr_findings_missing_rule_id():
    schema = load_schema("gdpr.findings.ready.v1.schema.json")
    event = sample_event("gdpr.findings.ready.v1")
    del event["payload"]["findings"][0]["rule_id"]
    with pytest.raises(ValidationError):
        validate(event, schema)


def test_gdpr_findings_invalid_start_offset_type():
    schema = load_schema("gdpr.findings.ready.v1.schema.json")
    event = sample_event("gdpr.findings.ready.v1")
    event["payload"]["findings"][0]["start_offset"] = "0"
    with pytest.raises(ValidationError):
        validate(event, schema)


def test_legal_findings_snippet_too_long():
    schema = load_schema("legal.findings.ready.v1.schema.json")
    event = sample_event("legal.findings.ready.v1")
    event["payload"]["findings"][0]["snippet"] = "a" * 6000
    with pytest.raises(ValidationError):
        validate(event, schema)


TOPICS = [
    "client.contract.received.v1",
    "document.extracted.v1",
    "document.segmented.v1",
    "gdpr.findings.ready.v1",
    "legal.findings.ready.v1",
    "gc.assessment.ready.v1",
    "report.published.v1",
]


for topic in TOPICS:
    def make_test(t=topic):  # capture topic
        def _test():
            schema = load_schema(f"{t}.schema.json")
            event = sample_event(t)
            validate(event, schema)
        return _test

    globals()[f"test_{topic.replace('.', '_')}"] = make_test()
