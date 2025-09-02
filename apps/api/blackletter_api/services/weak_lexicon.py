from __future__ import annotations
from functools import lru_cache
from typing import List

from .rulepack_loader import load_rulepack, Lexicon

DEFAULT_WEAK_TERMS = ["may", "might", "could", "should"]
DEFAULT_STRENGTHENERS = ["must", "shall"]


@lru_cache(maxsize=1)
def _load() -> Lexicon | None:
    rp = load_rulepack()
    return rp.lexicon if rp else None


@lru_cache(maxsize=1)
def get_weak_terms() -> List[str]:
    lex = _load()
    if not lex:
        return DEFAULT_WEAK_TERMS.copy()
    terms = [*(lex.hedging or []), *(lex.discretionary or []), *(lex.vague or [])]
    return terms or DEFAULT_WEAK_TERMS.copy()


@lru_cache(maxsize=1)
def get_counter_anchors() -> List[str]:
    lex = _load()
    if not lex:
        return DEFAULT_STRENGTHENERS.copy()
    anchors = list(lex.strengtheners or [])
    return anchors or DEFAULT_STRENGTHENERS.copy()


def get_weak_terms_with_metadata() -> List[tuple[str, str]]:
    """Return weak terms paired with category metadata."""
    lex = _load()
    if not lex:
        return [(t, "default") for t in DEFAULT_WEAK_TERMS]
    pairs = []
    pairs += [(t, "hedging") for t in lex.hedging]
    pairs += [(t, "discretionary") for t in lex.discretionary]
    pairs += [(t, "vague") for t in lex.vague]
    return pairs or [(t, "default") for t in DEFAULT_WEAK_TERMS]

