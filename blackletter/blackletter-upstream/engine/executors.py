import re
from typing import Iterable, Dict, Any, List
from .rules import Rule


def execute_rules(rules: Iterable[Rule], chunks: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply rules to chunks and return list of findings."""
    findings: List[Dict[str, Any]] = []
    for chunk in chunks:
        chunk_id = chunk.get('chunk_id')
        text = chunk.get('text', '')
        for rule in rules:
            if rule.is_regex() and rule.pattern:
                match = re.search(rule.pattern, text, flags=re.IGNORECASE)
                if match:
                    findings.append({
                        'rule_id': rule.id,
                        'chunk_id': chunk_id,
                        'snippet': match.group(0),
                        'severity': rule.severity,
                    })
            elif rule.is_keyword() and rule.keywords:
                lowered = text.lower()
                if all(kw.lower() in lowered for kw in rule.keywords):
                    findings.append({
                        'rule_id': rule.id,
                        'chunk_id': chunk_id,
                        'snippet': text,
                        'severity': rule.severity,
                    })
    return findings
