from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

BASE_DIR = Path(__file__).resolve().parents[1]
RULES_DIR = BASE_DIR / "rules"


class RulepackError(RuntimeError):
    """Raised when a rulepack cannot be loaded or is invalid."""


@dataclass
class DetectorSpec:
    id: str
    type: str
    description: Optional[str] = None
    lexicon: Optional[str] = None


@dataclass
class Lexicon:
    name: str
    terms: List[str]


@dataclass
class Rulepack:
    name: str
    version: str
    detectors: List[DetectorSpec] = field(default_factory=list)
    lexicons: Dict[str, Lexicon] = field(default_factory=dict)


def _load_yaml_file(p: Path) -> Dict[str, Any]:
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def api_rules_summary() -> Dict[str, Any]:
    rp = load_rulepack()
    if not rp:
        return {"packs": 0, "total_terms": 0, "by_pack": []}
    total_terms = sum(len(lx.terms) for lx in rp.lexicons.values())
    return {
        "packs": 1,
        "total_terms": total_terms,
        "by_pack": [
            {
                "id": rp.name,
                "version": rp.version,
                "hedging": total_terms,
                "discretionary": 0,
                "vague": 0,
                "regex": 0,
            }
        ],
    }


class RulepackLoader:
    def __init__(self, rules_dir: Path = RULES_DIR, rulepack_file: str = "art28_v1.yaml", app_env: str = "dev"):
        self.rules_dir = rules_dir
        self.rulepack_file = rulepack_file
        self.app_env = app_env
        self._cache: Optional[Rulepack] = None

    def load(self) -> Rulepack:
        if self._cache:
            return self._cache
        path = self.rules_dir / self.rulepack_file
        if not path.exists():
            raise RulepackError("rulepack file not found")
        data = _load_yaml_file(path)
        detectors = [
            DetectorSpec(
                id=d.get("id"),
                type=d.get("type", "lexicon"),
                description=d.get("description"),
                lexicon=(d.get("lexicon") or "").rsplit(".", 1)[0] or None,
            )
            for d in data.get("detectors", [])
        ]
        if not detectors:
            raise RulepackError("missing detectors")
        lexicons: Dict[str, Lexicon] = {}
        for lx in data.get("lexicons", []):
            file = lx.get("file")
            if not file:
                continue
            lex_data = _load_yaml_file(self.rules_dir / "lexicons" / file)
            name = lex_data.get("name") or file.rsplit(".", 1)[0]
            terms = [str(t) for t in lex_data.get("terms", [])]
            lexicons[name] = Lexicon(name=name, terms=terms)
        rp = Rulepack(
            name=data.get("name", "unknown"),
            version=data.get("version", "0"),
            detectors=detectors,
            lexicons=lexicons,
        )
        self._cache = rp
        return rp


def load_rulepack() -> Rulepack | None:
    try:
        return RulepackLoader().load()
    except RulepackError:
        return None


__all__ = [
    "RulepackError",
    "RulepackLoader",
    "Rulepack",
    "Lexicon",
    "DetectorSpec",
    "api_rules_summary",
    "load_rulepack",
]

# Backwards compatible aliases
Detector = DetectorSpec
