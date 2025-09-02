from __future__ import annotations

import os
import re
import json
from typing import Iterable, List, Optional, Dict, Any, Pattern

from .weak_lexicon import (
    get_weak_terms,
    get_counter_anchors,
)
from .detector_mapping import decide_verdict_with_downgrade
from .token_ledger import get_token_ledger, should_apply_token_capping, token_capping_enabled
from .rulepack_loader import load_rulepack
from packages.shared.python.types import Finding
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
    """Downgrade verdict if weak terms appear without counter-anchors."""
    if enabled is None:
        enabled = weak_lexicon_enabled()
    if not enabled or original_verdict != "pass":
        return original_verdict

    weak_terms = get_weak_terms()
    anchors = list(counter_anchors or []) + get_counter_anchors()
    verdict, _ = decide_verdict_with_downgrade(window_text, weak_terms, anchors)
    if verdict == "warn":
        return "weak"
    return original_verdict


def run_detectors(analysis_id: str, extraction_json_path: str) -> List[Finding]:
    """Minimal detector runner for lexicon and regex checks with token tracking."""
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

    # Estimate tokens for this analysis (rough approximation)
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

    # Precompile regex detectors once to avoid repeated compilation
    compiled_regexes: Dict[str, Pattern[str]] = {}
    for det in rulepack.detectors:
        if det.type == "regex" and det.pattern:
            try:
                compiled_regexes[det.id] = re.compile(det.pattern, re.IGNORECASE)
            except re.error:
                # Skip malformed patterns
                continue

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

                # Prefer lexicon metadata from extraction.json if provided
                meta = sentence_data.get("lexicon", {})
                hits = meta.get(name) or meta.get(lexicon_ref) or []
                if hits:
                    for hit in hits:
                        finding = Finding(
                            detector_id=detector_id,
                            rule_id=detector_id,
                            verdict="pass",
                            snippet=sentence_text,
                            page=page,
                            start=start,
                            end=end,
                            rationale="Lexicon term found.",
                            category=hit.get("category"),
                            confidence=hit.get("confidence"),
                        )
                        final_verdict = postprocess_weak_language(
                            original_verdict=finding.verdict,
                            window_text=finding.snippet
                        )
                        finding.verdict = final_verdict
                        findings.append(finding)
                    continue

                # Fallback to direct term matching if no metadata provided
                if lx.terms and isinstance(lx.terms[0], dict):
                    anchors_any = [item.get("term", "") for item in lx.terms if isinstance(item, dict)]
                else:
                    anchors_any = [str(term) for term in lx.terms]

                if _has_any(sentence_text.lower(), anchors_any):
                    finding = Finding(
                        detector_id=detector_id,
                        rule_id=detector_id,
                        verdict="pass",
                        snippet=sentence_text,
                        page=page,
                        start=start,
                        end=end,
                        rationale="Lexicon term found.",
                    )
                    final_verdict = postprocess_weak_language(
                        original_verdict=finding.verdict,
                        window_text=finding.snippet
                    )
                    finding.verdict = final_verdict
                    findings.append(finding)
            elif detector_spec.type == "regex":
                regex = compiled_regexes.get(detector_id)
                if regex and regex.search(sentence_text):
                    finding = Finding(
                        detector_id=detector_id,
                        rule_id=detector_id,
                        verdict="pass",
                        snippet=sentence_text,
                        page=page,
                        start=start,
                        end=end,
                        rationale=f"Regex pattern '{regex.pattern}' matched.",
                    )
                    final_verdict = postprocess_weak_language(
                        original_verdict=finding.verdict,
                        window_text=finding.snippet,
                    )
                    finding.verdict = final_verdict
                    findings.append(finding)

    # Persist findings
    a_dir = analysis_dir(analysis_id)
    findings_path = a_dir / "findings.json"
    with findings_path.open("w", encoding="utf-8") as f:
        json.dump([f.model_dump() for f in findings], f, indent=2)

    return findings
