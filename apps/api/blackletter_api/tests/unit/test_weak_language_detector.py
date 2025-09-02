from blackletter_api.core.weak_language_detector import evaluate_weak_language
from blackletter_api.services.lexicon_analyzer import Lexicon


def _mock_lexicon():
    return Lexicon(version="v1", language="en", hedging=["may"], strengtheners=["must", "shall"])


def test_weak_term_downgrades_without_counter_anchor(monkeypatch):
    monkeypatch.setenv("WEAK_LEXICON_ENABLED", "1")
    monkeypatch.setattr(
        "blackletter_api.core.weak_language_detector.load_lexicon",
        lambda language="en": _mock_lexicon(),
    )
    window = "The processor may process personal data where required."
    verdict, detected, version = evaluate_weak_language("pass", window)
    assert verdict == "weak"
    assert detected is True
    assert version == "v1"


def test_counter_anchor_prevents_downgrade(monkeypatch):
    monkeypatch.setenv("WEAK_LEXICON_ENABLED", "1")
    monkeypatch.setattr(
        "blackletter_api.core.weak_language_detector.load_lexicon",
        lambda language="en": _mock_lexicon(),
    )
    window = "The processor may process data, but must comply with controller instructions."
    verdict, detected, _ = evaluate_weak_language("pass", window, counter_anchors=["must", "shall"])
    assert verdict == "pass"
    assert detected is False


def test_toggle_off_preserves_verdict(monkeypatch):
    monkeypatch.setenv("WEAK_LEXICON_ENABLED", "0")
    monkeypatch.setattr(
        "blackletter_api.core.weak_language_detector.load_lexicon",
        lambda language="en": _mock_lexicon(),
    )
    window = "Processor may consider appropriate measures."
    verdict, detected, _ = evaluate_weak_language("pass", window)
    assert verdict == "pass"
    assert detected is False


def test_lexicon_loads_terms(monkeypatch):
    monkeypatch.setattr(
        "blackletter_api.services.lexicon_analyzer.load_lexicon",
        lambda language="en", force_reload=False: _mock_lexicon(),
    )
    from blackletter_api.services.lexicon_analyzer import load_lexicon

    lex = load_lexicon()
    assert "may" in lex.weak_terms()
