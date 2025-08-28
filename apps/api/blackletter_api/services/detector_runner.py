from __future__ import annotations

import os
import re
import json
from typing import Iterable, List, Optional, Dict, Any

from .weak_lexicon import get_weak_terms
from ..models.schemas import Finding
from .storage import analysis_dir


def weak_lexicon_enabled() -> bool:
    return os.getenv("WEAK_LEXICON_ENABLED", "1") == "1"


def _has_any(text_lc: str, terms: Iterable[str]) -> bool:
    for t in terms:
        if not t:
            continue
        # whole-word match, case-insensitive handled by pre-lowering text
        if re.search(rf"\b{re.escape(t)}\b", text_lc):
            return True
    return False


def postprocess_weak_language(
    original_verdict: str,
    window_text: str,
    counter_anchors: Optional[List[str]] = None,
    enabled: Optional[bool] = None,
) -> str:
    """Downgrade 'pass' to 'weak' if weak-language terms are present."""
    if enabled is None:
        enabled = weak_lexicon_enabled()
    if not enabled:
        return original_verdict

    terms = get_weak_terms()
    if not terms:
        return original_verdict

    text_lc = (window_text or "").lower()
    if counter_anchors:
        anchors_lc = [a.lower() for a in counter_anchors if a]
        if _has_any(text_lc, anchors_lc):
            return original_verdict

    if original_verdict == "pass" and _has_any(text_lc, terms):
        return "weak"
    return original_verdict


def run_detectors(analysis_id: str, extraction_json_path: str) -> List[Finding]:
    """Minimal detector runner for lexicon-based checks."""
    # For now, this is a placeholder. It should load a rulepack,
    # iterate through detectors, and generate findings.
    # This minimal version will just return a dummy finding.
    
    # In a real implementation, you would load the extraction data
    # with open(extraction_json_path, 'r') as f:
    #     extraction_data = json.load(f)

    # Dummy finding for demonstration
    dummy_finding = Finding(
        detector_id="D001",
        rule_id="R001",
        verdict="pass",
        snippet="This is a sample text.",
        page=1,
        start=0,
        end=22,
        rationale="Initial pass verdict."
    )

    # Apply post-processing
    final_verdict = postprocess_weak_language(
        original_verdict=dummy_finding.verdict,
        window_text=dummy_finding.snippet
    )
    dummy_finding.verdict = final_verdict

    findings = [dummy_finding]

    # Persist findings
    a_dir = analysis_dir(analysis_id)
    findings_path = a_dir / "findings.json"
    with findings_path.open("w", encoding="utf-8") as f:
        # Pydantic models need to be dumped to dicts for JSON serialization
        json.dump([f.model_dump() for f in findings], f, indent=2)

    return findings

