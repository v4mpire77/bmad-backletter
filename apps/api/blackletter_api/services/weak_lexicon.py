from __future__ import annotations

from functools import lru_cache
from typing import List

from .rulepack_loader import load_rulepack


@lru_cache(maxsize=1)
def get_weak_terms() -> List[str]:
    """Return normalized weak-language terms from the bundled lexicon.

    Loads rulepack and fetches the 'weak_language' lexicon terms. Returns
    lowercase, stripped terms suitable for exact term matching.
    """
    rp = load_rulepack()
    lx = rp.lexicons.get("weak_language") if rp and rp.lexicons else None
    if not lx or not lx.terms:
        return []
    return [str(t).strip().lower() for t in lx.terms if str(t).strip()]


@lru_cache(maxsize=1)
def get_weak_counter_anchors() -> List[str]:
    """Return normalized counter-anchors for weak-language from the rulepack.

    Fallback to an empty list when not provided. Normalized to lowercase and stripped.
    """
    rp = load_rulepack()
    lx = rp.lexicons.get("weak_language") if rp and rp.lexicons else None
    if not lx:
        return []
    anchors = getattr(lx, "counter_anchors", None) or []
    return [str(a).strip().lower() for a in anchors if str(a).strip()]