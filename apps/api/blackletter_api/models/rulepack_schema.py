"""Rulepack schema validation models with proper error reporting."""
from __future__ import annotations

import re
from typing import Any, List, Optional, Union, Literal

from pydantic import BaseModel, Field, ValidationError, field_validator


class RulepackValidationError(Exception):
    """Raised when a rulepack fails validation with detailed error information."""

    def __init__(self, message: str, field: str | None = None, value: Any | None = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(message)


class Version:
    """Semantic versioning helper class."""

    def __init__(self, version_str: str):
        if not re.match(r"^\d+\.\d+\.\d+$", version_str):
            raise ValueError(f"Invalid semantic version format: {version_str}")
        self.version_str = version_str
        self.parts = tuple(map(int, version_str.split(".")))
        self.major, self.minor, self.patch = self.parts

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.version_str

    def _coerce(self, other: Any) -> tuple[int, int, int] | Any:
        if isinstance(other, Version):
            return other.parts
        if isinstance(other, str):
            return Version(other).parts
        return NotImplemented

    def __eq__(self, other: Any) -> bool:  # pragma: no cover - simple
        other_parts = self._coerce(other)
        if other_parts is NotImplemented:
            return False
        return self.parts == other_parts

    def __lt__(self, other: Any) -> bool:
        other_parts = self._coerce(other)
        if other_parts is NotImplemented:
            return NotImplemented
        return self.parts < other_parts

    def __le__(self, other: Any) -> bool:
        other_parts = self._coerce(other)
        if other_parts is NotImplemented:
            return NotImplemented
        return self.parts <= other_parts

    def __gt__(self, other: Any) -> bool:
        other_parts = self._coerce(other)
        if other_parts is NotImplemented:
            return NotImplemented
        return self.parts > other_parts

    def __ge__(self, other: Any) -> bool:
        other_parts = self._coerce(other)
        if other_parts is NotImplemented:
            return NotImplemented
        return self.parts >= other_parts


def compare_versions(version1: str, version2: str) -> int:
    """Compare two semantic versions.

    Returns 0 if equal, -1 if version1 < version2, 1 if version1 > version2.
    """
    v1 = Version(version1)
    v2 = Version(version2)
    if v1.parts == v2.parts:
        return 0
    return -1 if v1.parts < v2.parts else 1


class WeakNearby(BaseModel):
    any: Union[List[str], str, None] = None
    all: Union[List[str], str, None] = None

    @field_validator("any", "all")
    def validate_patterns(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            if not v.startswith("@"):
                raise RulepackValidationError(
                    f"String patterns must start with '@' for references, got: {v}",
                    field="weak_nearby.pattern",
                    value=v,
                )
        elif isinstance(v, list):
            for pattern in v:
                if not isinstance(pattern, str):
                    raise RulepackValidationError(
                        f"All patterns must be strings, got: {type(pattern)}",
                        field="weak_nearby.pattern",
                        value=pattern,
                    )
        return v


class Detector(BaseModel):
    id: str = Field(..., min_length=1, max_length=100)
    anchors_any: Optional[List[str]] = None
    anchors_all: Optional[List[str]] = None
    allow_carveouts: Optional[List[str]] = None
    weak_nearby: Optional[WeakNearby] = None
    redflags_any: Optional[List[str]] = None
    flowdown_any: Optional[List[str]] = None
    copies_any: Optional[List[str]] = None
    audits_any: Optional[List[str]] = None

    @field_validator("id")
    def validate_id(cls, v: str) -> str:
        if not v:
            raise RulepackValidationError(
                "Detector ID cannot be empty",
                field="detector.id",
                value=v,
            )
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise RulepackValidationError(
                f"Detector ID must contain only alphanumeric characters, underscores, or hyphens: {v}",
                field="detector.id",
                value=v,
            )
        return v

    @field_validator(
        "anchors_any",
        "anchors_all",
        "allow_carveouts",
        "redflags_any",
        "flowdown_any",
        "copies_any",
        "audits_any",
    )
    def validate_pattern_lists(cls, v, info):
        if v is None:
            return v
        if not isinstance(v, list):
            raise RulepackValidationError(
                f"Pattern fields must be lists, got: {type(v)}",
                field=f"detector.{info.field_name}",
                value=v,
            )
        for pattern in v:
            if not isinstance(pattern, str):
                raise RulepackValidationError(
                    f"All patterns must be strings, got: {type(pattern)}",
                    field=f"detector.{info.field_name}",
                    value=pattern,
                )
            if not pattern.strip():
                raise RulepackValidationError(
                    f"Pattern cannot be empty or whitespace only: '{pattern}'",
                    field=f"detector.{info.field_name}",
                    value=pattern,
                )
        return v


class Meta(BaseModel):
    pack_id: str = Field(..., min_length=1, max_length=100)
    version: str = Field(..., pattern=r"^\d+\.\d+\.\d+$")
    evidence_window_sentences: int = Field(ge=1)
    verdicts: List[Literal["pass", "weak", "missing", "needs_review"]]
    tokenizer: str = "sentence"
    author: Optional[str] = None
    created_date: Optional[str] = None

    @field_validator("pack_id")
    def validate_pack_id(cls, v: str) -> str:
        if not v:
            raise RulepackValidationError(
                "Pack ID cannot be empty",
                field="meta.pack_id",
                value=v,
            )
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise RulepackValidationError(
                f"Pack ID must contain only alphanumeric characters, underscores, or hyphens: {v}",
                field="meta.pack_id",
                value=v,
            )
        return v

    @field_validator("version")
    def validate_version(cls, v: str) -> str:
        if not re.match(r"^\d+\.\d+\.\d+$", v):
            raise RulepackValidationError(
                f"Invalid semantic version format: {v}. Expected format: MAJOR.MINOR.PATCH",
                field="meta.version",
                value=v,
            )
        return v

    @field_validator("verdicts")
    def validate_verdicts(cls, v: List[str]) -> List[str]:
        if not v:
            raise RulepackValidationError(
                "Verdicts list cannot be empty",
                field="meta.verdicts",
                value=v,
            )
        valid_verdicts = {"pass", "weak", "missing", "needs_review"}
        for verdict in v:
            if verdict not in valid_verdicts:
                raise RulepackValidationError(
                    f"Invalid verdict: {verdict}. Must be one of: {valid_verdicts}",
                    field="meta.verdicts",
                    value=verdict,
                )
        return v


class Rulepack(BaseModel):
    meta: Meta
    shared_lexicon: dict[str, Any]
    Detectors: List[Detector]


def validate_rulepack(data: dict[str, Any]) -> Rulepack:
    """Validate rulepack data and return a Rulepack model."""
    try:
        rulepack = Rulepack.parse_obj(data)
    except RulepackValidationError:
        raise
    except ValidationError as exc:
        first = exc.errors()[0]
        field = ".".join(str(loc) for loc in first.get("loc", []))
        value = first.get("input")
        raise RulepackValidationError(first.get("msg", "validation error"), field=field, value=value)

    ids = [det.id for det in rulepack.Detectors]
    if len(ids) != len(set(ids)):
        raise RulepackValidationError("Duplicate detector IDs found", field="Detectors", value=ids)

    return rulepack
