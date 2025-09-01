"""Core analysis logic for the GDPR rules engine."""

from __future__ import annotations

import logging
import re
from typing import List, Optional

from .models import Issue, Playbook, RuleOverride, RulesConfig
from .segment import segment_clauses

logger = logging.getLogger(__name__)

DEFAULT_VAGUE_TERMS = [
    "reasonable",
    "reasonably",
    "undue delay",
    "promptly",
    "as soon as possible",
    "as soon as practicable",
    "best efforts",
    "commercially reasonable",
    "material",
    "substantial",
    "substantially",
    "appropriate",
    "if appropriate",
    "adequate",
    "satisfactory",
    "sufficient",
]


def analyze_document(
    doc_id: str,
    text: str,
    rules_config: RulesConfig,
    playbook: Optional[Playbook] = None,
) -> List[Issue]:
    """Analyze ``text`` against GDPR ``rules_config`` and optional ``playbook``.

    Returns a list of :class:`Issue` objects describing rule coverage and
    vague term occurrences.
    """

    clauses = segment_clauses(text)
    issues: List[Issue] = []
    full_text_lower = text.lower()

    if playbook is None:
        playbook = Playbook()
    overrides = playbook.rules

    for rule in rules_config.rules:
        if rule.id in overrides and overrides[rule.id].enabled is False:
            continue

        effective_sev = overrides.get(rule.id, RuleOverride()).severity or rule.severity

        keywords = [kw.lower() for kw in rule.primary_keywords]
        aliases = [al.lower() for al in rule.aliases]
        if rule.id in overrides:
            keywords += [kw.lower() for kw in overrides[rule.id].add_keywords or []]
            aliases += [al.lower() for al in overrides[rule.id].add_aliases or []]

        kw_patterns = [
            re.compile(r"\b" + re.escape(kw) + r"\b", re.IGNORECASE) for kw in keywords
        ]
        alias_patterns = [
            re.compile(r"\b" + re.escape(al) + r"\b", re.IGNORECASE) for al in aliases
        ]

        found = False
        found_clause_id: Optional[str] = None
        snippet = ""
        matched_terms: List[str] = []

        for i, clause in enumerate(clauses):
            context_parts = []
            for j in range(i - 2, i + 3):
                if 0 <= j < len(clauses):
                    context_parts.append(clauses[j]["text"])
            context_text = " ".join(context_parts).lower()

            found_kw = any(p.search(context_text) for p in kw_patterns)
            found_al = any(p.search(context_text) for p in alias_patterns)
            if found_kw or found_al:
                found = True
                found_clause_id = clause["id"]
                clause_text = clause["text"].strip()
                snippet = clause_text[:200] + ("..." if len(clause_text) > 200 else "")
                for p, term in zip(kw_patterns, keywords):
                    if p.search(context_text):
                        matched_terms.append(term)
                for p, term in zip(alias_patterns, aliases):
                    if p.search(context_text):
                        matched_terms.append(term)
                break

        if found:
            rationale_text = f"Clause covers requirement: {rule.description}"
            status = "found"
        else:
            rationale_text = f"No clause found covering: {rule.description}"
            status = "missing"
            found_clause_id = None
            snippet = ""
            matched_terms = []

        issues.append(
            Issue(
                id=f"{doc_id}_{rule.id}",
                doc_id=doc_id,
                rule_id=rule.id,
                clause_path=found_clause_id,
                snippet=snippet,
                citation=None,
                rationale=rationale_text,
                severity=effective_sev,
                status=status,
                raw_matches={"keywords": matched_terms},
                rule_scores={
                    "primary_found": any(term in keywords for term in matched_terms),
                    "alias_found": any(term in aliases for term in matched_terms),
                },
            )
        )

    if playbook.enable_vague_terms_scan:
        extra_vagues: List[str] = []
        if "VAGUE_TERMS_EXTRA" in playbook.rules:
            extra_vagues = [
                t.lower()
                for t in playbook.rules["VAGUE_TERMS_EXTRA"].add_keywords or []
            ]
        vague_terms = [t.lower() for t in DEFAULT_VAGUE_TERMS] + extra_vagues
        for term in vague_terms:
            if term in full_text_lower:
                idx = full_text_lower.index(term)
                snippet_start = max(0, idx - 40)
                snippet_end = min(len(text), idx + len(term) + 40)
                vague_snip = text[snippet_start:snippet_end].strip()
                issues.append(
                    Issue(
                        id=f"{doc_id}_VAGUE_{term}",
                        doc_id=doc_id,
                        rule_id="VAGUE_TERM",
                        clause_path=None,
                        snippet=vague_snip + ("..." if snippet_end < len(text) else ""),
                        citation=None,
                        rationale=f"Vague term '{term}' found, which may cause ambiguity",
                        severity="Low",
                        status="review",
                        raw_matches={"term": [term]},
                        rule_scores={"vague_term_found": True},
                    )
                )

    logger.info("Rule engine completed: %d issues", len(issues))
    return issues
