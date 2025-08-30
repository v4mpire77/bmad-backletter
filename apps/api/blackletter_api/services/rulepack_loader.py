from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any

import yaml
import os
import logging


DEFAULT_RULEPACK_VERSION = "art28_v1"
logger = logging.getLogger(__name__)


@dataclass
class Lexicon:
    name: str
    terms: List[Any]
    counter_anchors: Optional[List[str]] = None


@dataclass
class Detector:
    id: str
    type: str
    description: Optional[str] = None
    lexicon: Optional[str] = None


@dataclass
class Rulepack:
    name: str
    version: str
    detectors: List[Detector]
    lexicons: Dict[str, Lexicon]


class RulepackError(Exception):
    pass


def resolve_rulepack_version(requested_version: Optional[str] = None) -> str:
    return requested_version or DEFAULT_RULEPACK_VERSION


def _rules_dir() -> Path:
    env_dir = os.getenv("RULES_DIR")
    if env_dir:
        return Path(env_dir)
    return Path(__file__).resolve().parent.parent / "rules"


def load_rulepack(version: Optional[str] = None, load_lexicons: bool = True) -> Rulepack:
    """Load a rulepack YAML and associated lexicons into structured objects.

    The default rulepack is apps/api/blackletter_api/rules/art28_v1.yaml
    """
    ver = resolve_rulepack_version(version)
    rules_directory = _rules_dir()
    env_file = os.getenv("RULEPACK_FILE")
    if env_file:
        rulepack_path = rules_directory / env_file
    else:
        rulepack_path = rules_directory / f"{ver}.yaml"
    if not rulepack_path.exists():
        raise RulepackError(f"rulepack_not_found: {ver}")

    with rulepack_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    name = str(data.get("name") or "art28")
    rp_version = str(data.get("version") or "v1")

    detectors: List[Detector] = []
    for d in data.get("detectors", []) or []:
        detectors.append(
            Detector(
                id=str(d.get("id")),
                type=str(d.get("type")),
                description=d.get("description"),
                lexicon=d.get("lexicon"),
            )
        )
    if not detectors:
        raise RulepackError("invalid_rulepack: no detectors defined")

    # Load lexicons referenced in rulepack (either via top-level list or on detectors)
    lexicons: Dict[str, Lexicon] = {}
    lex_dir = rules_directory / "lexicons"

    def _load_lexicon_file(filename: str) -> Lexicon:
        p = lex_dir / filename
        if not p.exists():
            raise RulepackError(f"lexicon_not_found: {filename}")
        try:
            with p.open("r", encoding="utf-8") as lf:
                lx_data = yaml.safe_load(lf) or {}
        except Exception as e:
            logger.warning(f"Failed to parse lexicon {filename}: {e}; using empty lexicon")
            lx_data = {"name": filename.rsplit(".", 1)[0], "terms": []}
        terms = lx_data.get("terms") or lx_data.get("weak_terms") or []
        counter_anchors = lx_data.get("counter_anchors")
        name = str(lx_data.get("name") or filename.rsplit(".", 1)[0])
        return Lexicon(name=name, terms=terms, counter_anchors=counter_anchors)

    # Explicit lexicons list in rulepack
    if load_lexicons:
        for item in data.get("lexicons", []) or []:
            file = item.get("file") if isinstance(item, dict) else str(item)
            if not file:
                continue
            lx = _load_lexicon_file(file)
            # store under both hyphen and underscore variants
            lexicons[lx.name] = lx
            lexicons[lx.name.replace("-", "_")] = lx

    # Ensure any lexicon referenced by detectors is also loaded
    if load_lexicons:
        for det in detectors:
            ref = det.lexicon
            if not ref:
                continue
            fname = ref if ref.endswith(".yaml") else f"{ref}"
            if fname not in {k if k.endswith('.yaml') else f"{k}.yaml" for k in lexicons.keys()}:
                # derive filename from ref
                actual = ref if ref.endswith(".yaml") else f"{ref}.yaml"
                lx = _load_lexicon_file(actual)
                lexicons[lx.name] = lx
                lexicons[lx.name.replace("-", "_")] = lx

    return Rulepack(name=name, version=rp_version, detectors=detectors, lexicons=lexicons)


def get_rulepack_metadata(version: Optional[str] = None) -> tuple[str, str]:
    rp = load_rulepack(version=version, load_lexicons=False)
    return rp.name, rp.version


class RulepackLoader:
    def __init__(self, rules_dir: Path, rulepack_file: str = "art28_v1.yaml", app_env: str | None = None):
        self.rules_dir = Path(rules_dir)
        self.rulepack_file = rulepack_file
        self.app_env = app_env or os.getenv("APP_ENV", "dev")

    def load(self) -> Rulepack:
        old_rules_dir = os.getenv("RULES_DIR")
        old_file = os.getenv("RULEPACK_FILE")
        try:
            os.environ["RULES_DIR"] = str(self.rules_dir)
            os.environ["RULEPACK_FILE"] = self.rulepack_file
            return load_rulepack(load_lexicons=True)
        finally:
            if old_rules_dir is not None:
                os.environ["RULES_DIR"] = old_rules_dir
            else:
                os.environ.pop("RULES_DIR", None)
            if old_file is not None:
                os.environ["RULEPACK_FILE"] = old_file
            else:
                os.environ.pop("RULEPACK_FILE", None)


def get_rulepack_metadata(version: Optional[str] = None) -> tuple[str, str]:
    """Return (name, version) without loading lexicons."""
    rp = load_rulepack(version=version, load_lexicons=False)
    return rp.name, rp.version
