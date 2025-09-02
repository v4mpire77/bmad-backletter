from threading import Thread

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


def test_concurrent_advance_no_keyerror_or_lost_updates():
    orch = Orchestrator()
    analysis_id = orch.intake("contract.docx")

    def worker(i: int) -> None:
        orch.advance(analysis_id, AnalysisState.EXTRACTED, {"issue": i})

    threads = [Thread(target=worker, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    record = orch.summary(analysis_id)
    assert record.state == AnalysisState.EXTRACTED
    assert sorted(f["issue"] for f in record.findings) == list(range(5))
