from blackletter_api.models.schemas import Rulepack, Detector
from blackletter_api.services.detector_engine import evaluate


def make_rulepack() -> Rulepack:
    det = Detector(
        id="d1",
        anchors_any=["must"],
        redflags_any=["forbidden"],
        weak_nearby={"any": "@hedges"},
    )
    return Rulepack(
        meta={},
        detectors=[det],
        shared_lexicon={"hedges": ["may"]},
    )


def test_evaluate_variants() -> None:
    rp = make_rulepack()
    det = rp.detectors[0]

    flags = evaluate("must act", det, rp)
    assert flags == {"anchor": True, "weak": False, "redflag": False}

    flags = evaluate("must act and may stop", det, rp)
    assert flags["anchor"] and flags["weak"]

    flags = evaluate("must act though forbidden", det, rp)
    assert flags["redflag"]
