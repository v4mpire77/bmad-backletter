from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

import yaml
from redis import Redis

BASE_DIR = Path(__file__).resolve().parents[1]
LEXICON_DIR = BASE_DIR / "rules" / "lexicons"

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
try:
    redis_client: Redis | None = Redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
except Exception:  # pragma: no cover - gracefully handle missing redis
    redis_client = None

CACHE_PREFIX = "lexicon_cache:"


@dataclass
class Lexicon:
    version: str = "0"
    language: str = "en"
    hedging: List[str] = field(default_factory=list)
    discretionary: List[str] = field(default_factory=list)
    vague: List[str] = field(default_factory=list)
    strengtheners: List[str] = field(default_factory=list)

    def weak_terms(self) -> List[str]:
        return [*self.hedging, *self.discretionary, *self.vague]


@lru_cache(maxsize=16)
def _load_from_disk(language: str) -> Lexicon:
    """Load lexicon YAML for a given language from disk."""
    candidates = [
        LEXICON_DIR / f"weak_language_{language}.yaml",
        LEXICON_DIR / language / "weak_language.yaml",
    ]
    if language == "en":
        candidates.append(LEXICON_DIR / "weak_language.yaml")
    for path in candidates:
        if path.exists():
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            return Lexicon(
                version=str(data.get("version") or data.get("lexicon_id") or "0"),
                language=str(data.get("language") or language),
                hedging=list(data.get("hedges") or data.get("hedging") or []),
                discretionary=list(data.get("discretion") or data.get("discretionary") or []),
                vague=list(
                    data.get("ambiguity")
                    or data.get("vagueness")
                    or data.get("vague")
                    or data.get("vagueness_time")
                    or []
                ),
                strengtheners=list(
                    [
                        *(
                            data.get("strengtheners")
                            or data.get("anchors", {}).get("strengtheners")
                            or []
                        ),
                        *(data.get("counter_anchors") or []),
                    ]
                ),
            )
    return Lexicon(language=language)


def load_lexicon(language: str = "en", force_reload: bool = False) -> Lexicon:
    """Load lexicon, using Redis cache when available."""
    cache_key = f"{CACHE_PREFIX}{language}"
    if not force_reload and redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            data = json.loads(cached)
            return Lexicon(**data)

    lex = _load_from_disk(language)
    if redis_client:
        redis_client.set(cache_key, json.dumps(lex.__dict__))
    return lex


def list_lexicons() -> List[Dict[str, str]]:
    """List available lexicon files with language and version."""
    lexicons: List[Dict[str, str]] = []
    for path in LEXICON_DIR.rglob("*.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        language = data.get("language") or path.stem.split("_")[-1]
        version = str(data.get("version") or data.get("lexicon_id") or "0")
        lexicons.append({"file": path.name, "language": language, "version": version})
    return lexicons


def reload_lexicons() -> None:
    """Clear caches to force lexicon reload."""
    _load_from_disk.cache_clear()
    if redis_client:
        keys = redis_client.keys(f"{CACHE_PREFIX}*")
        if keys:
            redis_client.delete(*keys)
