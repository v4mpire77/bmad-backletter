from __future__ import annotations

import re
from typing import Dict, List

from ..models.schemas import Detector, Rulepack


def _resolve_terms(raw: object, rulepack: Rulepack) -> List[str]:
    """Resolve term lists that may reference shared lexicons."""
    if raw is None:
        return []
    if isinstance(raw, str):
        if raw.startswith("@"):
            return rulepack.shared_lexicon.get(raw[1:], [])
        return [raw]
    terms: List[str] = []
    for item in raw:  # type: ignore[assignment]
        if isinstance(item, str) and item.startswith("@"):
            terms.extend(rulepack.shared_lexicon.get(item[1:], []))
        else:
            terms.append(str(item))
    return terms


def evaluate(text: str, detector: Detector, rulepack: Rulepack) -> Dict[str, bool]:
    """Evaluate a single detector against text.

    Returns dict with keys: anchor, weak, redflag.
    """
    def _match(pattern: str) -> bool:
        try:
            return bool(re.search(pattern, text, flags=re.IGNORECASE))
        except re.error:
            raise

    anchor = False
    if detector.anchors_all:
        anchor = all(_match(p) for p in detector.anchors_all)
    elif detector.anchors_any:
        anchor = any(_match(p) for p in detector.anchors_any)

    weak_terms = _resolve_terms(
        getattr(detector, "weak_nearby", {}).get("any"), rulepack
    )
    weak = any(_match(t) for t in weak_terms) if weak_terms else False

    red_terms = detector.redflags_any or []
    redflag = any(_match(t) for t in red_terms) if red_terms else False

    return {"anchor": anchor, "weak": weak, "redflag": redflag}
