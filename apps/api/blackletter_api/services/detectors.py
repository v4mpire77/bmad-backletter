from __future__ import annotations

import re
from typing import Any, Dict, List


def run_detectors(text: str, rulepack: Dict[str, Any]) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    rules = rulepack.get("rules", [])
    lowered = text.lower()

    for rule in rules:
        rid = rule.get("id", "unknown")
        rtype = rule.get("type")
        count = 0
        if rtype == "keyword":
            for kw in rule.get("keywords", []) or []:
                if not isinstance(kw, str):
                    continue
                count += lowered.count(kw.lower())
        elif rtype == "regex":
            pat = rule.get("pattern")
            if isinstance(pat, str):
                try:
                    count = len(re.findall(pat, text))
                except re.error:
                    count = 0
        else:
            continue

        findings.append({"rule_id": rid, "count": count})

    return {
        "version": rulepack.get("version"),
        "findings": findings,
    }

