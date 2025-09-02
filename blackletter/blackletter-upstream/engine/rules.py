from dataclasses import dataclass
from typing import List, Optional
import yaml


@dataclass
class Rule:
    """Representation of a compliance rule loaded from YAML."""
    id: str
    title: str
    severity: str
    guidance: str
    citations: List[str]
    pattern: Optional[str] = None
    keywords: Optional[List[str]] = None

    def is_regex(self) -> bool:
        return self.pattern is not None

    def is_keyword(self) -> bool:
        return self.keywords is not None


def load_rules(path: str) -> List[Rule]:
    """Load a YAML rule file into a list of Rule objects."""
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or []

    rules: List[Rule] = []
    for raw in data:
        rule = Rule(
            id=raw['id'],
            title=raw.get('title', ''),
            severity=raw.get('severity', 'medium'),
            guidance=raw.get('guidance', ''),
            citations=raw.get('citations', []),
            pattern=raw.get('pattern'),
            keywords=raw.get('keywords'),
        )
        rules.append(rule)
    return rules
