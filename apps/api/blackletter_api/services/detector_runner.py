from __future__ import annotations

import os
import re
import json
from typing import Iterable, List, Optional, Dict, Any

from .weak_lexicon import (
    get_weak_terms,
    get_weak_terms_with_metadata,
    get_counter_anchors,
    calculate_weak_confidence,
    get_terms_by_confidence_threshold
)
from .token_ledger import get_token_ledger, should_apply_token_capping, token_capping_enabled
from .rulepack_loader import load_rulepack
from ..models.schemas import Finding
from .storage import analysis_dir
from .evidence import build_window


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
    confidence_threshold: float = 0.5,
) -> str:
    """Downgrade 'pass' to 'weak' if weak-language terms are present, with confidence scoring."""
    if enabled is None:
        enabled = weak_lexicon_enabled()
    if not enabled:
        return original_verdict

    text_lc = (window_text or "").lower()

    # Check counter-anchors first (they prevent downgrade)
    all_counter_anchors = []
    if counter_anchors:
        all_counter_anchors.extend([a.lower() for a in counter_anchors if a])
    # Add lexicon counter-anchors
    lexicon_counter_anchors = get_counter_anchors()
    all_counter_anchors.extend(lexicon_counter_anchors)

    if all_counter_anchors and _has_any(text_lc, all_counter_anchors):
        return original_verdict

    # Use enhanced weak language detection with confidence scoring
    weak_terms = get_weak_terms_with_metadata()
    if not weak_terms:
        return original_verdict

    has_weak, confidence, category = calculate_weak_confidence(text_lc, weak_terms)

    if original_verdict == "pass" and has_weak and confidence >= confidence_threshold:
        return "weak"
    return original_verdict


def run_detectors(analysis_id: str, extraction_json_path: str) -> List[Finding]:
    """Minimal detector runner for lexicon-based checks with token tracking."""
    findings: List[Finding] = []

    # Initialize token tracking
    ledger = get_token_ledger()
    apply_capping = should_apply_token_capping()
    cap_exceeded = False
    cap_reason = None

    # Load extraction data
    with open(extraction_json_path, 'r', encoding="utf-8") as f:
        extraction_data = json.load(f)

    sentences = extraction_data.get("sentences", [])
    total_sentences = len(sentences)

    # Estimate tokens for this analysis (rough approximation)
    # ~4 characters per token, plus some overhead
    estimated_chars = sum(len(s.get("text", "")) for s in sentences)
    estimated_tokens = max(100, (estimated_chars // 4) + 50)  # Minimum 100 tokens + overhead

    # Check token cap before processing if capping is enabled
    if apply_capping:
        cap_exceeded, cap_reason = ledger.add_tokens(
            analysis_id=analysis_id,
            input_tokens=estimated_tokens,
            output_tokens=0  # No LLM output in lexicon-based detection
        )

        if cap_exceeded:
            # Create a special finding for token cap exceeded
            cap_finding = Finding(
                detector_id="token_cap",
                rule_id="token_cap",
                verdict="needs_review",
                snippet=f"Analysis stopped due to token cap: {cap_reason}",
                page=1,
                start=0,
                end=0,
                rationale=f"Token usage limit exceeded. {cap_reason}"
            )
            findings.append(cap_finding)

            # Persist findings early and return
            a_dir = analysis_dir(analysis_id)
            findings_path = a_dir / "findings.json"
            with findings_path.open("w", encoding="utf-8") as f:
                json.dump([f.model_dump() for f in findings], f, indent=2)

            return findings

    # Load rulepack dynamically
    rulepack = load_rulepack()

    processed_sentences = 0
    # Evidence window sizing (default +/- 2 sentences)
    try:
        window_before = int(os.getenv("EVIDENCE_WINDOW_BEFORE", "2"))
    except ValueError:
        window_before = 2
    try:
        window_after = int(os.getenv("EVIDENCE_WINDOW_AFTER", "2"))
    except ValueError:
        window_after = 2
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

                # Extract terms list from lexicon (handle both old and new formats)
                if lx.terms and isinstance(lx.terms[0], dict):
                    anchors_any = [item.get("term", "") for item in lx.terms if isinstance(item, dict)]
                else:
                    anchors_any = [str(term) for term in lx.terms]

                if _has_any(sentence_text.lower(), anchors_any):
                    # Build evidence window around the sentence span (page-scoped)
                    window = build_window(
                        sentences=sentences,
                        target_page=page,
                        target_span=(start, end),
                        before=window_before,
                        after=window_after,
                    )

                    finding = Finding(
                        detector_id=detector_id,
                        rule_id=detector_id,  # Use detector_id as rule_id for now
                        verdict="pass",
                        snippet=window.get("text", sentence_text),
                        page=window.get("page", page),
                        start=window.get("start", start),
                        end=window.get("end", end),
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

        processed_sentences += 1

    # Persist findings
    a_dir = analysis_dir(analysis_id)
    findings_path = a_dir / "findings.json"
    with findings_path.open("w", encoding="utf-8") as f:
        json.dump([f.model_dump() for f in findings], f, indent=2)

    return findings
