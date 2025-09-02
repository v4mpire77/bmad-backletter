from __future__ import annotations

import os
import re
from typing import List, Optional, Tuple

from ..services.lexicon_analyzer import load_lexicon


def weak_lexicon_enabled() -> bool:
    """Check environment flag for weak language detection."""
    return os.getenv("WEAK_LEXICON_ENABLED", "1") == "1"


def evaluate_weak_language(
    original_verdict: str,
    window_text: str,
    language: str = "en",
    counter_anchors: Optional[List[str]] = None,
) -> Tuple[str, bool, str]:
    """Apply weak language analysis to an evidence window.

    Returns a tuple of (new_verdict, weak_language_detected, lexicon_version).
    """
    lexicon = load_lexicon(language)
    version = lexicon.version

    if not weak_lexicon_enabled() or original_verdict != "pass":
        return original_verdict, False, version

    text_lc = window_text.lower()
    weak_terms = lexicon.weak_terms()
    if any(re.search(rf"\b{re.escape(t)}\b", text_lc) for t in weak_terms):
        anchors = [*(counter_anchors or []), *lexicon.strengtheners]
        if not any(re.search(rf"\b{re.escape(a)}\b", text_lc) for a in anchors):
            return "weak", True, version
    return original_verdict, False, version
