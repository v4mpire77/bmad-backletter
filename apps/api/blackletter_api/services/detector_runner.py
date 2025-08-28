from __future__ import annotations

import os
import re
import json
from typing import Iterable, List, Optional, Dict, Any

from .weak_lexicon import get_weak_terms
from .rulepack_loader import load_rulepack
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
    findings: List[Finding] = []

    # Load extraction data
    with open(extraction_json_path, 'r', encoding="utf-8") as f:
        extraction_data = json.load(f)

    sentences = extraction_data.get("sentences", [])

    # Load rulepack dynamically
    rulepack = load_rulepack()

    for sentence_data in sentences:
        sentence_text = sentence_data.get("text", "")
        page = sentence_data.get("page", 1)
        start = sentence_data.get("start", 0)
        end = sentence_data.get("end", 0)

        for detector_spec in rulepack.detectors:
            detector_id = detector_spec.id
            

            if detector_spec.type == "lexicon":
                lexicon_ref = detector_spec.lexicon or ""
                # Normalize: allow filename (weak_language.yaml), name (weak_language), or hyphenated variants
                name = (
                    lexicon_ref.rsplit('.', 1)[0]
                    if isinstance(lexicon_ref, str) and lexicon_ref.endswith('.yaml')
                    else lexicon_ref
                )
                name = str(name).replace('-', '_')
                lx = rulepack.lexicons.get(name) or rulepack.lexicons.get(lexicon_ref)
                if not lx or not lx.terms:
                    # Skip if lexicon missing or empty
                    continue
                anchors_any = lx.terms

                if _has_any(sentence_text.lower(), anchors_any):
                    finding = Finding(
                        detector_id=detector_id,
                        rule_id=detector_id, # Use detector_id as rule_id for now
                        verdict="pass",
                        snippet=sentence_text,
                        page=page,
                        start=start,
                        end=end,
                        rationale="Lexicon term found."
                    )

                    final_verdict = postprocess_weak_language(
                        original_verdict=finding.verdict,
                        window_text=finding.snippet
                    )
                    finding.verdict = final_verdict
                    findings.append(finding)
            elif detector_spec.type == "regex":
                # TODO: Implement regex detector logic
                pass # For now, skip regex detectors

    # Persist findings
    a_dir = analysis_dir(analysis_id)
    findings_path = a_dir / "findings.json"
    with findings_path.open("w", encoding="utf-8") as f:
        json.dump([f.model_dump() for f in findings], f, indent=2)

    return findings
