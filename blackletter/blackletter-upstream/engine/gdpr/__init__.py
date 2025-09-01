"""GDPR rules engine package."""

from .engine import DEFAULT_VAGUE_TERMS, analyze_document
from .models import Issue, Playbook, Rule, RuleOverride, RulesConfig
from .segment import segment_clauses

__all__ = [
    "Issue",
    "Playbook",
    "Rule",
    "RuleOverride",
    "RulesConfig",
    "segment_clauses",
    "analyze_document",
    "DEFAULT_VAGUE_TERMS",
]
