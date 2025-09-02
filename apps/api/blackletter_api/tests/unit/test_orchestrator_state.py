from blackletter_api.orchestrator.state import Orchestrator, AnalysisState


def test_advance_updates_state_and_findings():
    orch = Orchestrator()
    analysis_id = orch.intake("contract.pdf")
    result = orch.advance(analysis_id, AnalysisState.EXTRACTED, {"issue": "ok"})
    assert result.state == AnalysisState.EXTRACTED
    assert orch.findings(analysis_id) == [{"issue": "ok"}]


def test_advance_without_finding():
    orch = Orchestrator()
    analysis_id = orch.intake("contract.docx")
    orch.advance(analysis_id, AnalysisState.SEGMENTED)
    record = orch.summary(analysis_id)
    assert record.state == AnalysisState.SEGMENTED
    assert record.findings == []
