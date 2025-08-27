from __future__ import annotations

import os
import threading
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel, Field, ValidationError, root_validator


class RulepackError(Exception):
    """Raised when rulepack loading or validation fails."""


class Lexicon(BaseModel):
    name: str
    terms: List[str] = Field(default_factory=list)


class Detector(BaseModel):
    id: str
    type: str = Field(description="Detector type: e.g., 'lexicon', 'regex', 'anchor'")
    description: Optional[str] = None
    # For regex detectors
    pattern: Optional[str] = None
    # For lexicon detectors, reference to a lexicon name or file
    lexicon: Optional[str] = None

    @root_validator
    def validate_detector(cls, values):
        det_type = values.get("type")
        pattern = values.get("pattern")
        lexicon = values.get("lexicon")

        if det_type == "regex" and not pattern:
            raise ValueError("regex detector requires 'pattern'")
        if det_type == "lexicon" and not lexicon:
            raise ValueError("lexicon detector requires 'lexicon'")
        return values


class Rulepack(BaseModel):
    name: str
    version: str
    detectors: List[Detector]
    # Loaded lexicons by name
    lexicons: Dict[str, Lexicon] = Field(default_factory=dict)


class RulepackLoader:
    """Loads a versioned rulepack YAML and associated lexicons from a directory.

    Environment-configurable via:
      - RULES_DIR: base directory containing rulepack file and lexicons/
      - RULEPACK_FILE: rulepack YAML filename (default: art28_v1.yaml)
      - APP_ENV: 'dev' or 'prod' (hot reload disabled for 'prod')
    """

    def __init__(
        self,
        rules_dir: Path,
        rulepack_file: str = "art28_v1.yaml",
        app_env: str = os.getenv("APP_ENV", "dev"),
    ) -> None:
        self.rules_dir = Path(rules_dir)
        self.rulepack_file = rulepack_file
        self.app_env = app_env
        self._cache_lock = threading.Lock()
        self._cached: Optional[Rulepack] = None

    @property
    def hot_reload(self) -> bool:
        # Hot reload disabled in production
        return self.app_env.lower() != "prod"

    def _rulepack_path(self) -> Path:
        return self.rules_dir / self.rulepack_file

    def load(self, force: bool = False) -> Rulepack:
        if not force and not self.hot_reload and self._cached is not None:
            return self._cached

        with self._cache_lock:
            if not force and not self.hot_reload and self._cached is not None:
                return self._cached
            try:
                rp_data = self._load_rulepack_yaml()
                rulepack = self._validate_and_assemble(rp_data)
            except (OSError, yaml.YAMLError, ValidationError, ValueError) as e:
                raise RulepackError(str(e)) from e

            if not self.hot_reload:
                self._cached = rulepack
            return rulepack

    def _load_rulepack_yaml(self) -> dict:
        path = self._rulepack_path()
        if not path.exists():
            raise FileNotFoundError(f"Rulepack file not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if not isinstance(data, dict):
            raise ValueError("Rulepack YAML must be a mapping at the top level")
        return data

    def _validate_and_assemble(self, data: dict) -> Rulepack:
        # Basic required fields
        name = data.get("name") or data.get("id") or "unknown"
        version = data.get("version") or data.get("ver") or "v1"
        detectors_raw = data.get("detectors")
        if not isinstance(detectors_raw, list) or not detectors_raw:
            raise ValueError("Rulepack must define a non-empty 'detectors' list")

        detectors: List[Detector] = [Detector(**d) for d in detectors_raw]

        # Load lexicons referenced by detectors or specified under data['lexicons']
        lexicons_dir = self.rules_dir / "lexicons"
        provided_lexicons = data.get("lexicons")
        lexicons: Dict[str, Lexicon] = {}

        def load_lexicon_file(file_name: str) -> Lexicon:
            path = lexicons_dir / file_name
            if not path.exists():
                raise FileNotFoundError(f"Lexicon file not found: {path}")
            with path.open("r", encoding="utf-8") as f:
                lx = yaml.safe_load(f) or {}
            if isinstance(lx, dict) and "terms" in lx:
                name = lx.get("name") or Path(file_name).stem
                terms = lx.get("terms") or []
                if not isinstance(terms, list):
                    raise ValueError(f"Lexicon '{name}' terms must be a list")
                return Lexicon(name=name, terms=[str(t) for t in terms])
            elif isinstance(lx, list):
                # allow list-of-terms without wrapper
                name = Path(file_name).stem
                return Lexicon(name=name, terms=[str(t) for t in lx])
            else:
                raise ValueError(f"Invalid lexicon format in {file_name}")

        # Load any lexicons explicitly listed
        if isinstance(provided_lexicons, list):
            for item in provided_lexicons:
                if isinstance(item, dict) and "file" in item:
                    lx = load_lexicon_file(str(item["file"]))
                    lexicons[lx.name] = lx
                elif isinstance(item, str):
                    lx = load_lexicon_file(item)
                    lexicons[lx.name] = lx
                else:
                    raise ValueError("Each lexicon entry must be a filename or {file: name}")

        # Load lexicons referenced by detectors if missing
        for det in detectors:
            if det.lexicon:
                ref = det.lexicon
                # Accept either lexicon name previously loaded or a filename
                if ref in lexicons:
                    continue
                # Try as filename
                try:
                    lx = load_lexicon_file(ref)
                    lexicons[lx.name] = lx
                except FileNotFoundError:
                    # Keep as a name-only reference; must exist among loaded lexicons
                    if ref not in lexicons:
                        raise ValueError(
                            f"Detector '{det.id}' references unknown lexicon '{ref}'"
                        )

        return Rulepack(name=name, version=version, detectors=detectors, lexicons=lexicons)


@lru_cache(maxsize=1)
def get_default_loader() -> RulepackLoader:
    base_dir = os.getenv(
        "RULES_DIR",
        str(Path(__file__).resolve().parent / ".." / "rules"),
    )
    rulepack_file = os.getenv("RULEPACK_FILE", "art28_v1.yaml")
    app_env = os.getenv("APP_ENV", "dev")
    return RulepackLoader(Path(base_dir).resolve(), rulepack_file=rulepack_file, app_env=app_env)


def load_rulepack(force: bool = False) -> Rulepack:
    loader = get_default_loader()
    return loader.load(force=force)

