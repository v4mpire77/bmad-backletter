from __future__ import annotations

from blackletter_api.services.detector_runner import postprocess_weak_language
from blackletter_api.services.weak_lexicon import get_weak_terms


def test_weak_term_downgrades_without_counter_anchor(monkeypatch):
    # Ensure feature is on
    monkeypatch.setenv("WEAK_LEXICON_ENABLED", "1")
    # Avoid rulepack counter-anchors (e.g., 'required')
    window = "The processor may process personal data."
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


def test_rulepack_counter_anchors_used_by_default(monkeypatch):
    # Uses rulepack-provided counter_anchors (must/shall/required) without passing explicitly
    monkeypatch.setenv("WEAK_LEXICON_ENABLED", "1")
    window = "The processor may process data but must comply with instructions."
    verdict = postprocess_weak_language("pass", window_text=window, counter_anchors=None)
    assert verdict == "pass"


def test_whole_word_matching_not_partial(monkeypatch):
    monkeypatch.setenv("WEAK_LEXICON_ENABLED", "1")
    window = "This clause discusses mayhem but is otherwise strict."
    verdict = postprocess_weak_language("pass", window_text=window, counter_anchors=None)
    # 'mayhem' should not trigger 'may' due to whole-word boundary
    assert verdict == "pass"


def test_case_insensitive_matching(monkeypatch):
    monkeypatch.setenv("WEAK_LEXICON_ENABLED", "1")
    window = "The controller MAY adopt measures."
    verdict = postprocess_weak_language("pass", window_text=window, counter_anchors=None)
    assert verdict == "weak"