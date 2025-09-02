"""Rulepack schema validation models."""
from __future__ import annotations

from typing import Any, Literal, Union
from pydantic import BaseModel, Field


class WeakNearby(BaseModel):
    any: Union[list[str], str, None] = None  # Allow string references like "@hedges"
    all: Union[list[str], str, None] = None


class Detector(BaseModel):
    id: str
    anchors_any: list[str] | None = None
    anchors_all: list[str] | None = None
    allow_carveouts: list[str] | None = None
    weak_nearby: WeakNearby | None = None
    redflags_any: list[str] | None = None
    flowdown_any: list[str] | None = None
    copies_any: list[str] | None = None
    audits_any: list[str] | None = None


class Meta(BaseModel):
    pack_id: str
    evidence_window_sentences: int = Field(ge=1)
    verdicts: list[Literal['pass','weak','missing','needs_review']]
    tokenizer: str = "sentence"


class Rulepack(BaseModel):
    meta: Meta
    shared_lexicon: dict[str, Any]
    Detectors: list[Detector]