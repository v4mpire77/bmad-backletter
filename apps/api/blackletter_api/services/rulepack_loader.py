from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

# repo root is two levels up from services; adjust to find bundled rules
BASE_DIR = Path(__file__).resolve().parents[1]
RULES_DIR = BASE_DIR / "rules"


@dataclass
class Lexicon:
    hedging: List[str] = field(default_factory=list)
    discretionary: List[str] = field(default_factory=list)
    vague: List[str] = field(default_factory=list)
    strengtheners: List[str] = field(default_factory=list)


@dataclass
class Rulepack:
    id: str
    version: str
    lexicon: Lexicon
    regex_rules: List[Dict[str, Any]]
    author: Optional[str] = None
    created_at: Optional[str] = None


class RulepackError(Exception):
    """Raised when rulepack metadata cannot be loaded."""


def _safe_list(x) -> List[str]:
    if not x:
        return []
    return [str(s).strip() for s in x if str(s).strip()]


def _load_yaml_file(p: Path) -> Dict[str, Any]:
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_rulepacks() -> List[Rulepack]:
    """Load all rulepacks from /rules/*.yml|*.yaml (absolute path)."""
    if not RULES_DIR.exists():
        return []
    files = sorted([*RULES_DIR.glob("*.yml"), *RULES_DIR.glob("*.yaml")])
    packs: List[Rulepack] = []
    for f in files:
        data = _load_yaml_file(f)
        meta = data.get("meta", {})
        lex = data.get("weak_language", {})
        anchors = data.get("anchors", {})
        packs.append(
            Rulepack(
                id=str(meta.get("id") or f.stem),
                version=str(meta.get("version") or "0.0.0"),
                lexicon=Lexicon(
                    hedging=_safe_list(lex.get("hedging")),
                    discretionary=_safe_list(lex.get("discretionary")),
                    vague=_safe_list(lex.get("vague")),
                    strengtheners=_safe_list(anchors.get("strengtheners")),
                ),
                regex_rules=list(data.get("regex_rules") or []),
                author=meta.get("author"),
                created_at=meta.get("created_at"),
            )
        )
    return packs


def api_rules_summary() -> Dict[str, Any]:
    """Small summary used by tests & /rules routes."""
    packs = load_rulepacks()
    total_terms = sum(
        len(p.lexicon.hedging) + len(p.lexicon.discretionary) + len(p.lexicon.vague)
        for p in packs
    )
    return {
        "packs": len(packs),
        "total_terms": total_terms,
        "by_pack": [
            {
                "id": p.id,
                "version": p.version,
                "hedging": len(p.lexicon.hedging),
                "discretionary": len(p.lexicon.discretionary),
                "vague": len(p.lexicon.vague),
                "regex": len(p.regex_rules),
            }
            for p in packs
        ],
    }


# Backwards/explicit export so tests doing `from ... import api_rules_summary` don't crash
__all__ = [
    "Lexicon",
    "Rulepack",
    "RulepackError",
    "load_rulepacks",
    "api_rules_summary",
    "load_rulepack",
    "list_rulepack_metadata",
]


def load_rulepack() -> Rulepack | None:
    packs = load_rulepacks()
    return packs[0] if packs else None


def list_rulepack_metadata() -> List[Dict[str, Any]]:
    """Return metadata for available rulepacks."""
    packs = load_rulepacks()
    if not packs:
        raise RulepackError("No rulepacks available")
    return [
        {
            "id": p.id,
            "version": p.version,
            "author": p.author,
            "created_at": p.created_at,
        }
        for p in packs
    ]


