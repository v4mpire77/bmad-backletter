from __future__ import annotations

import os
import re
import json
from typing import Iterable, List, Optional, Dict, Any

from .weak_lexicon import get_weak_terms, get_weak_counter_anchors
from .rulepack_loader import load_rulepack
from .evidence import build_configurable_window
from ..models.schemas import Finding
from .storage import analysis_dir
from ..core_config_loader import load_core_config
from .token_ledger import add_tokens, llm_provider_enabled, get_ledger, reset_ledger


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
    # If not explicitly provided, use rulepack-sourced counter anchors
    anchors_source = counter_anchors if counter_anchors is not None else get_weak_counter_anchors()
    if anchors_source:
        anchors_lc = [a.lower() for a in anchors_source if a]
        if _has_any(text_lc, anchors_lc):
            return original_verdict

    if original_verdict == "pass" and _has_any(text_lc, terms):
        return "weak"
    return original_verdict


def run_detectors(analysis_id: str, extraction_json_path: str) -> List[Finding]:
    """Enhanced detector runner with evidence window support (Story 1.3)."""
    findings: List[Finding] = []

    # Load extraction data
    with open(extraction_json_path, 'r', encoding="utf-8") as f:
        extraction_data = json.load(f)

    sentences = extraction_data.get("sentences", [])
    
    # Load core configuration for default window size
    core_config = load_core_config()
    default_window_size = core_config.evidence_window_sentences

    # Persist zeroed ledger if provider disabled to ensure persistence visibility in metrics
    if not llm_provider_enabled():
        reset_ledger(analysis_id)

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
                    # Build evidence window around the finding using Story 1.3 functionality
                    detector_config = getattr(detector_spec, 'config', {}) or {}
                    evidence_window = build_configurable_window(
                        sentences=sentences,
                        target_page=page,
                        target_span=(start, end),
                        detector_config=detector_config,
                        default_window_size=default_window_size
                    )
                    
                    # Simulate token usage for evidence window building path only when provider enabled
                    if llm_provider_enabled():
                        # Rough token estimate: 1 token per 4 chars of evidence text (MVP heuristic)
                        approx_tokens = max(1, len(evidence_window["text"]) // 4)
                        add_tokens(analysis_id, approx_tokens)

                    finding = Finding(
                        detector_id=detector_id,
                        rule_id=detector_id, # Use detector_id as rule_id for now
                        verdict="pass",
                        # For snippet, tests expect the exact sentence text, not the full window
                        snippet=sentence_text,
                        page=page,
                        # Keep original sentence boundaries for start/end to match snippet
                        start=start,
                        end=end,
                        rationale=f"Lexicon term found. Evidence window: ±{evidence_window['window_size']['before']}/±{evidence_window['window_size']['after']} sentences."
                    )

                    # Apply weak language processing to the evidence window
                    final_verdict = postprocess_weak_language(
                        original_verdict=finding.verdict,
                        window_text=evidence_window["text"]  # Use full evidence window for weak language analysis
                    )
                    finding.verdict = final_verdict

                    # If cap exceeded, mark finding as needs_review and short-circuit LLM-dependent paths
                    ledger = get_ledger(analysis_id)
                    if ledger.needs_review:
                        finding.verdict = "needs_review"
                        finding.rationale += " Cap exceeded; LLM paths short-circuited."
                    findings.append(finding)
            elif detector_spec.type == "regex":
                # TODO: Implement regex detector logic with evidence windows
                pass # For now, skip regex detectors

    # Persist findings
    a_dir = analysis_dir(analysis_id)
    findings_path = a_dir / "findings.json"
    with findings_path.open("w", encoding="utf-8") as f:
        json.dump([f.model_dump() for f in findings], f, indent=2)

    return findings