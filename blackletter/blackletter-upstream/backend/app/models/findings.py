from typing import List, Literal
from pydantic import BaseModel
from .rules import Severity

# Citation model (reused from rules)
class Citation(BaseModel):
    doc_id: str
    page: int
    start: int
    end: int

Verdict = Literal["compliant","non_compliant","weak","insufficient_context"]

class Quote(BaseModel):
    text: str
    citation: Citation

class Finding(BaseModel):
    rule_id: str
    severity: Severity
    verdict: Verdict
    risk: Literal["low","medium","high"]
    rationale: str
    snippet: str
    improvements: List[str] = []
    quotes: List[Quote] = []