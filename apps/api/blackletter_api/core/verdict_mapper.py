from __future__ import annotations

from typing import Tuple


def map_verdict(anchor: bool, weak: bool, redflag: bool) -> Tuple[str, float]:
    """Map detector signal combination to a verdict with confidence.

    Args:
        anchor: Whether an anchor pattern was detected.
        weak: Whether weak language was detected near the anchor.
        redflag: Whether a red‑flag term was detected.

    Returns:
        A tuple of (verdict, confidence_score).
    """
    if redflag:
        return "needs_review", 0.1
    if anchor and weak:
        return "weak", 0.5
    if anchor:
        return "pass", 1.0
    return "missing", 0.0
