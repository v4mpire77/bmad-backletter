from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Dict, Iterable, List, Optional, Pattern

from sqlalchemy.exc import SQLAlchemyError

from ..core.weak_language_detector import evaluate_weak_language
from ..database import SessionLocal
from ..models.entities import OrgSetting
from ..models.schemas import Finding
from .evidence import build_window
from .rulepack_loader import load_rulepack
from .storage import analysis_dir
from .token_ledger import (
    get_token_ledger,
    should_apply_token_capping,
)

logger = logging.getLogger(__name__)


def _has_any(text_lc: str, terms: Iterable[str]) -> bool:
    for t in terms:
        if not t:
            continue
        # whole-word match, case-insensitive handled by pre-lowering text
        if re.search(rf"\b{re.escape(t)}\b", text_lc):
            return True
    return False


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
            cap_message = f"Analysis stopped due to token cap: {cap_reason}"
            cap_finding = Finding(
                detector_id="token_cap",
                rule_id="token_cap",
                verdict="needs_review",
                snippet=cap_message,
                original_text=cap_message,
                suggested_text=None,
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

    n_sentences = 2
    try:
        with SessionLocal() as db:
            settings = db.query(OrgSetting).first()
            if settings and getattr(settings, "evidence_window_sentences", None):
                n_sentences = settings.evidence_window_sentences
    except SQLAlchemyError:
        pass

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
                            original_text=sentence_text,
                            suggested_text=None,
                            page=page,
                            start=start,
                            end=end,
                            rationale="Lexicon term found.",
                            category=hit.get("category"),
                            confidence=hit.get("confidence"),
                        )
                        new_verdict, detected, version = evaluate_weak_language(
                            original_verdict=finding.verdict,
                            window_text=finding.snippet,
                        )
                        if new_verdict != finding.verdict:
                            logger.debug(
                                "weak language verdict change: %s -> %s",
                                finding.verdict,
                                new_verdict,
                            )
                        finding.verdict = new_verdict
                        finding.weak_language_detected = detected
                        finding.lexicon_version = version
                        findings.append(finding)
                    continue

                # Fallback to direct term matching if no metadata provided
                if lx.terms and isinstance(lx.terms[0], dict):
                    anchors_any = [item.get("term", "") for item in lx.terms if isinstance(item, dict)]
                else:
                    anchors_any = [str(term) for term in lx.terms]

                if _has_any(sentence_text.lower(), anchors_any):
                    window = build_window(analysis_id, start, end, n_sentences=n_sentences)
                    snippet = window["snippet"] or sentence_text
                    page_val = window["page"] or page
                    start_val = window["start"] or start
                    end_val = window["end"] or end
                    finding = Finding(
                        detector_id=detector_id,
                        rule_id=detector_id,
                        verdict="pass",
                        snippet=snippet,
                        original_text=window["snippet"] or sentence_text,
                        suggested_text=None,
                        page=page_val,
                        start=start_val,
                        end=end_val,
                        rationale="Lexicon term found.",
                    )
                    new_verdict, detected, version = evaluate_weak_language(
                        original_verdict=finding.verdict,
                        window_text=finding.snippet,
                    )
                    if new_verdict != finding.verdict:
                        logger.debug(
                            "weak language verdict change: %s -> %s",
                            finding.verdict,
                            new_verdict,
                        )
                    finding.verdict = new_verdict
                    finding.weak_language_detected = detected
                    finding.lexicon_version = version
                    findings.append(finding)
            elif detector_spec.type == "regex":
                regex = compiled_regexes.get(detector_id)
                if regex and regex.search(sentence_text):
                    window = build_window(analysis_id, start, end, n_sentences=n_sentences)
                    snippet = window["snippet"] or sentence_text
                    page_val = window["page"] or page
                    start_val = window["start"] or start
                    end_val = window["end"] or end
                    finding = Finding(
                        detector_id=detector_id,
                        rule_id=detector_id,
                        verdict="pass",
                        snippet=snippet,
                        original_text=window["snippet"] or sentence_text,
                        suggested_text=None,
                        page=page_val,
                        start=start_val,
                        end=end_val,
                        rationale=f"Regex pattern '{regex.pattern}' matched.",
                    )
                    new_verdict, detected, version = evaluate_weak_language(
                        original_verdict=finding.verdict,
                        window_text=finding.snippet,
                    )
                    if new_verdict != finding.verdict:
                        logger.debug(
                            "weak language verdict change: %s -> %s",
                            finding.verdict,
                            new_verdict,
                        )
                    finding.verdict = new_verdict
                    finding.weak_language_detected = detected
                    finding.lexicon_version = version
                    findings.append(finding)

    # Persist findings
    a_dir = analysis_dir(analysis_id)
    findings_path = a_dir / "findings.json"
    with findings_path.open("w", encoding="utf-8") as f:
        json.dump([f.model_dump() for f in findings], f, indent=2)

    return findings
