from __future__ import annotations

from functools import lru_cache
from typing import List

from .lexicon_analyzer import load_lexicon

DEFAULT_WEAK_TERMS = ["may", "might", "could", "should"]
DEFAULT_STRENGTHENERS = ["must", "shall"]


@lru_cache(maxsize=1)
def get_weak_terms(language: str = "en") -> List[str]:
    lex = load_lexicon(language)
    terms = lex.weak_terms()
    return terms or DEFAULT_WEAK_TERMS.copy()


@lru_cache(maxsize=1)
def get_counter_anchors(language: str = "en") -> List[str]:
    lex = load_lexicon(language)
    anchors = list(lex.strengtheners)
    return anchors or DEFAULT_STRENGTHENERS.copy()
