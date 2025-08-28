from __future__ import annotations

from blackletter_api.services.detector_runner import postprocess_weak_language
from blackletter_api.services.weak_lexicon import get_weak_terms


def test_weak_term_downgrades_without_counter_anchor(monkeypatch):
    # Ensure feature is on
    monkeypatch.setenv("WEAK_LEXICON_ENABLED", "1")
    window = "The processor may process personal data where required."
    verdict = postprocess_weak_language("pass", window_text=window, counter_anchors=None)
    assert verdict == "weak"


def test_counter_anchor_prevents_downgrade(monkeypatch):
    monkeypatch.setenv("WEAK_LEXICON_ENABLED", "1")
    window = "The processor may process data, but must comply with controller instructions."
    verdict = postprocess_weak_language("pass", window_text=window, counter_anchors=["must", "shall"])
    assert verdict == "pass"


def test_toggle_off_preserves_verdict(monkeypatch):
    monkeypatch.setenv("WEAK_LEXICON_ENABLED", "0")
    window = "Processor may consider appropriate measures."
    verdict = postprocess_weak_language("pass", window_text=window, counter_anchors=None)
    assert verdict == "pass"


def test_lexicon_loads_terms():
    terms = get_weak_terms()
    assert isinstance(terms, list) and terms, "expected weak terms to load"
    assert "may" in terms

