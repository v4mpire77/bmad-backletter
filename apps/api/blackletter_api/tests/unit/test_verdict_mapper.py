from blackletter_api.core.verdict_mapper import map_verdict


def test_map_verdict_cases() -> None:
    assert map_verdict(True, False, False) == ("pass", 1.0)
    assert map_verdict(True, True, False) == ("weak", 0.5)
    assert map_verdict(False, False, False) == ("missing", 0.0)
    assert map_verdict(True, False, True)[0] == "needs_review"
