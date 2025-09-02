from __future__ import annotations
from typing import Iterable, Tuple
import re


def _any_term_present(text: str, terms: Iterable[str]) -> bool:
    if not terms:
        return False
    # word-ish matching; keep simple & deterministic
    pattern = r"|".join(re.escape(t) for t in terms if t)
    return bool(re.search(rf"\b(?:{pattern})\b", text, flags=re.I))


def decide_verdict_with_downgrade(
    text: str,
    weak_terms: Iterable[str],
    counter_anchors: Iterable[str],
) -> Tuple[str, str]:
    """
    Returns (verdict, reason)
    - If counter anchor (strong language) present, do NOT downgrade.
    - If no counter anchor and weak term present → downgrade to 'warn'.
    - Else 'pass'.
    """
    has_weak = _any_term_present(text, weak_terms)
    has_anchor = _any_term_present(text, counter_anchors)
    if has_anchor:
        return ("pass", "counter-anchor present")
    if has_weak:
        return ("warn", "weak term without counter-anchor")
    return ("pass", "no weak terms")

