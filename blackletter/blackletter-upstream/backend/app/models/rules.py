from typing import List, Dict, Literal, Optional, Union
from pydantic import BaseModel, Field, validator

Severity = Literal["critical","high","medium","low"]

class ScoringAdjust(BaseModel):
    condition: str
    delta: float

class BaseCheck(BaseModel):
    type: str
    field: Literal["full_text"] = "full_text"
    note: Optional[str] = None

class RegexAnyCheck(BaseCheck):
    type: Literal["regex_any"]
    patterns: List[str]
    min_hits: Optional[int] = 1

class RegexAllCheck(BaseCheck):
    type: Literal["regex_all"]
    patterns: List[str]

class NegationRegexCheck(BaseCheck):
    type: Literal["negation_regex"]
    pattern: str
    must_not_match: bool = True

class FlagIfOnlyVagueCheck(BaseCheck):
    type: Literal["flag_if_only_vague"]
    patterns: List[str]
    flag: Literal["amber","warn"] = "amber"

class ConditionalPassCheck(BaseCheck):
    type: Literal["conditional_pass"]
    condition: str

class PolicyEvaluateCheck(BaseCheck):
    type: Literal["policy_evaluate"]
    criteria: Dict[str, Dict[str, List[str]]]

RuleCheck = Union[
    RegexAnyCheck, RegexAllCheck, NegationRegexCheck,
    FlagIfOnlyVagueCheck, ConditionalPassCheck, PolicyEvaluateCheck
]

class RuleMessage(BaseModel):
    pass_: Optional[str] = Field(None, alias="pass")
    warn: Optional[str] = None
    fail: Optional[str] = None

class Rule(BaseModel):
    id: str
    name: str
    article: Optional[str]
    severity: Severity
    description: str
    required: bool = True
    checks: List[RuleCheck]
    messages: Optional[RuleMessage] = None
    scoring_adjustments: Optional[List[ScoringAdjust]] = None
    remediation: Optional[str] = None

class Scoring(BaseModel):
    weights: Dict[Severity, int]
    pass_threshold: float

class Meta(BaseModel):
    generated_at: Optional[str]
    purpose: Optional[str]
    scoring: Scoring

class RuleSet(BaseModel):
    version: str
    jurisdiction: List[str]
    meta: Meta
    rules: List[Rule]

    @validator("rules")
    def unique_ids(cls, v):
        ids = [r.id for r in v]
        dupes = set([i for i in ids if ids.count(i) > 1])
        if dupes:
            raise ValueError(f"duplicate rule ids: {', '.join(sorted(dupes))}")
        return v