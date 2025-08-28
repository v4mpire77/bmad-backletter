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

