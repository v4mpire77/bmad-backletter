"""Pydantic models for GDPR rules engine configuration and results."""

from typing import Dict, List, Optional

from pydantic import BaseModel


class Rule(BaseModel):
    """GDPR rule definition."""

    id: str
    description: str
    primary_keywords: List[str]
    aliases: List[str] = []
    severity: str = "Medium"


class RulesConfig(BaseModel):
    """Container for a collection of GDPR rules."""

    rules: List[Rule]


class RuleOverride(BaseModel):
    """Overrides for a single rule in a playbook."""

    enabled: Optional[bool] = None
    severity: Optional[str] = None
    add_keywords: List[str] = []
    add_aliases: List[str] = []


class Playbook(BaseModel):
    """Organization-specific playbook settings."""

    organization: Optional[str] = None
    enable_vague_terms_scan: Optional[bool] = None
    rules: Dict[str, RuleOverride] = {}


class Issue(BaseModel):
    """Result of a rule check or vague term detection."""

    id: str
    doc_id: str
    rule_id: str
    clause_path: Optional[str]
    snippet: str
    citation: Optional[str]
    rationale: str
    severity: str
    status: str
    raw_matches: Dict[str, List[str]]
    rule_scores: Dict[str, bool]
