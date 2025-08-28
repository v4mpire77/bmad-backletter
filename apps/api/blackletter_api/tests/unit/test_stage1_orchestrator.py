import json
from pathlib import Path

from jsonschema import validate

from blackletter_api.orchestrator.state import AnalysisState, orchestrator


def test_event_schema_validation():
    schema_path = Path(__file__).resolve().parents[5] / "contracts" / "events" / "client.contract.received.v1.schema.json"
    schema = json.loads(schema_path.read_text())
    event = {
        "event_id": "evt-1",
        "topic": "client.contract.received.v1",
        "analysis_id": "a1",
        "payload": {}
    }
    validate(instance=event, schema=schema)


def test_happy_path_orchestrator():
    orchestrator._analyses.clear()
    analysis = orchestrator.create()
    orchestrator.handle_event(analysis.id, "document.extracted.v1")
    orchestrator.handle_event(analysis.id, "document.segmented.v1")
    orchestrator.handle_event(analysis.id, "gdpr.findings.ready.v1", [])
    orchestrator.handle_event(analysis.id, "legal.findings.ready.v1", [])
    orchestrator.handle_event(analysis.id, "gc.assessment.ready.v1", [])
    orchestrator.handle_event(analysis.id, "report.published.v1")
    assert orchestrator.get(analysis.id).state == AnalysisState.REPORTED
