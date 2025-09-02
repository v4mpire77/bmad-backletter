from blackletter_api.models.schemas import Rulepack, Detector
from blackletter_api.services.analysis_orchestrator import run_analysis


def build_rulepack() -> Rulepack:
    good = Detector(id="a", anchors_any=["must"])
    bad = Detector(id="b", anchors_any=["("])  # invalid regex
    return Rulepack(meta={}, detectors=[bad, good], shared_lexicon={})


def test_run_analysis_handles_failures() -> None:
    rp = build_rulepack()
    findings = run_analysis("must comply", rp)
    assert [f.detector_id for f in findings] == ["a", "b"]
    verdicts = {f.detector_id: f.verdict for f in findings}
    assert verdicts["a"] == "pass"
    assert verdicts["b"] == "needs_review"
