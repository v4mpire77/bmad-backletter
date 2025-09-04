"""Rulepack schema validation models with proper error reporting."""
from __future__ import annotations

from typing import Any, Literal, Union, Optional, List
from pydantic import BaseModel, Field, field_validator
from pydantic import ValidationInfo
import re


class RulepackValidationError(Exception):
    """Raised when a rulepack fails validation with detailed error information."""

    def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.message)


class Version:
    """Semantic versioning helper class."""

    def __init__(self, version_str: str):
        if not re.match(r'^\d+\.\d+\.\d+', version_str):
            raise ValueError(f"Invalid semantic version format: {version_str}")
        self.version_str = version_str
        self.parts = tuple(map(int, version_str.split('.')))
        self.major, self.minor, self.patch = self.parts

    def __str__(self):
        return self.version_str

    def __eq__(self, other):
        if isinstance(other, str):
            return self.version_str == other
        if isinstance(other, Version):
            return self.parts == other.parts
        return False

    def __lt__(self, other):
        if isinstance(other, str):
            other = Version(other)
        elif not isinstance(other, Version):
            return NotImplemented
        return self.parts < other.parts

    def __le__(self, other):
        if isinstance(other, str):
            other = Version(other)
        elif not isinstance(other, Version):
            return NotImplemented
        return self.parts <= other.parts

    def __gt__(self, other):
        if isinstance(other, str):
            other = Version(other)
        elif not isinstance(other, Version):
            return NotImplemented
        return self.parts > other.parts

    def __ge__(self, other):
        if isinstance(other, str):
            other = Version(other)
        elif not isinstance(other, Version):
            return NotImplemented
        return self.parts >= other.parts


class WeakNearby(BaseModel):
    # Allow string references like "@hedges"
    any: Union[list[str], str, None] = None
    all: Union[list[str], str, None] = None

    @field_validator('any', 'all')
    def validate_patterns(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            # Allow string references like "@hedges"
            if not v.startswith('@'):
                raise RulepackValidationError(
                    f"String patterns must start with '@' for references, got: {v}",
                    field="weak_nearby.pattern",
                    value=v
                )
        elif isinstance(v, list):
            for pattern in v:
                if not isinstance(pattern, str):
                    raise RulepackValidationError(
                        f"All patterns must be strings, got: {type(pattern)}",
                        field="weak_nearby.pattern",
                        value=pattern
                    )
        return v


class Detector(BaseModel):
    id: str = Field(..., max_length=100)
    anchors_any: Optional[List[str]] = None
    anchors_all: Optional[List[str]] = None
    allow_carveouts: Optional[List[str]] = None
    weak_nearby: Optional[WeakNearby] = None
    redflags_any: Optional[List[str]] = None
    flowdown_any: Optional[List[str]] = None
    copies_any: Optional[List[str]] = None
    audits_any: Optional[List[str]] = None

    @field_validator('id')
    def validate_id(cls, v):
        if not v:
            raise RulepackValidationError(
                "Detector ID cannot be empty",
                field="detector.id",
                value=v
            )
        # Check for valid characters (alphanumeric, underscore, hyphen)
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise RulepackValidationError(
                f"Detector ID must contain only alphanumeric characters, underscores, or hyphens: {v}",
                field="detector.id",
                value=v
            )
        return v

    @field_validator(
        'anchors_any',
        'anchors_all',
        'allow_carveouts',
        'redflags_any',
        'flowdown_any',
        'copies_any',
        'audits_any',
        mode='after',
    )
    def validate_patterns(cls, v, info: ValidationInfo):
        if v is None:
            return v
        if not isinstance(v, list):
            raise RulepackValidationError(
                f"Pattern fields must be lists, got: {type(v)}",
                field=f"detector.{info.field_name}",
                value=v
            )
        for pattern in v:
            if not isinstance(pattern, str):
                raise RulepackValidationError(
                    f"All patterns must be strings, got: {type(pattern)}",
                    field=f"detector.{info.field_name}",
                    value=pattern
                )
            if not pattern.strip():
                raise RulepackValidationError(
                    f"Pattern cannot be empty or whitespace only: '{pattern}'",
                    field=f"detector.{info.field_name}",
                    value=pattern
                )
        return v


class Meta(BaseModel):
    pack_id: str = Field(..., min_length=1, max_length=100)
    version: str = Field(..., pattern=r'^\d+\.\d+\.\d+')  # Semantic versioning
    evidence_window_sentences: int = Field(ge=1, le=10)  # Reasonable limits
    verdicts: List[Literal['pass', 'weak', 'missing', 'needs_review']]
    tokenizer: str = "sentence"
    author: Optional[str] = None
    created_date: Optional[str] = None

    @field_validator('pack_id')
    def validate_pack_id(cls, v):
        if not v:
            raise RulepackValidationError(
                "Pack ID cannot be empty",
                field="meta.pack_id",
                value=v
            )
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9_-]+', v):
            raise RulepackValidationError(
                f"Pack ID must contain only alphanumeric characters, underscores, or hyphens: {v}",
                field="meta.pack_id",
                value=v
            )
        return v

    @field_validator('version')
    def validate_version(cls, v):
        # Simple semantic version validation (MAJOR.MINOR.PATCH)
        if not re.match(r'^\d+\.\d+\.\d+', v):
            raise RulepackValidationError(
                f"Invalid semantic version format: {v}. Expected format: MAJOR.MINOR.PATCH",
                field="meta.version",
                value=v
            )
        return v

    @field_validator('verdicts')
    def validate_verdicts(cls, v):
        if not v:
            raise RulepackValidationError(
                "Verdicts list cannot be empty",
                field="meta.verdicts",
                value=v
            )
        valid_verdicts = {'pass', 'weak', 'missing', 'needs_review'}
        for verdict in v:
            if verdict not in valid_verdicts:
                raise RulepackValidationError(
                    f"Invalid verdict: {verdict}. Must be one of: {valid_verdicts}",
                    field="meta.verdicts",
                    value=verdict
                )
        return v


class Rulepack(BaseModel):
    meta: Meta
    shared_lexicon: dict[str, Any] = Field(default_factory=dict)
    Detectors: List[Detector] = Field(..., min_length=1)

    @field_validator('Detectors')
    def validate_unique_detector_ids(cls, v):
        if not v:
            raise RulepackValidationError(
                "Rulepack must contain at least one detector",
                field="Detectors",
                value=v
            )
        detector_ids = [detector.id for detector in v]
        if len(detector_ids) != len(set(detector_ids)):
            duplicates = [
                id for id in detector_ids if detector_ids.count(id) > 1]
            raise RulepackValidationError(
                f"Duplicate detector IDs found: {set(duplicates)}",
                field="Detectors",
                value=duplicates
            )
        return v

    @field_validator('shared_lexicon')
    def validate_lexicon(cls, v):
        if not isinstance(v, dict):
            raise RulepackValidationError(
                f"Shared lexicon must be a dictionary, got: {type(v)}",
                field="shared_lexicon",
                value=v
            )
        for key, value in v.items():
            if not isinstance(key, str):
                raise RulepackValidationError(
                    f"Lexicon keys must be strings, got: {type(key)}",
                    field="shared_lexicon",
                    value=key
                )
            if not isinstance(value, (list, dict)):
                raise RulepackValidationError(
                    f"Lexicon values must be lists or dictionaries, got: {type(value)}",
                    field="shared_lexicon",
                    value=value
                )
        return v


def validate_rulepack(data: dict) -> Rulepack:
    """Validate rulepack data and return a validated Rulepack object."""
    try:
        return Rulepack(**data)
    except RulepackValidationError:
        # Preserve custom validation errors
        raise
    except Exception as e:
        if hasattr(e, 'errors'):
            errors = e.errors()
            if errors:
                error = errors[0]
                field = ".".join(str(loc) for loc in error['loc']) if error.get(
                    'loc') else None
                raise RulepackValidationError(
                    error['msg'],
                    field=field,
                    value=error.get('input')
                )
        raise RulepackValidationError(str(e))


def compare_versions(version1: str, version2: str) -> int:
    """
    Compare two semantic versions.

    Args:
        version1: First version string
        version2: Second version string

    Returns:
        int: -1 if version1 < version2, 0 if equal, 1 if version1 > version2
    """
    v1 = Version(version1)
    v2 = Version(version2)

    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        return 0
