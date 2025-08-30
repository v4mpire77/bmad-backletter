from __future__ import annotations

from typing import Optional


DEFAULT_RULEPACK_VERSION = "art28_v1"


def resolve_rulepack_version(requested_version: Optional[str] = None) -> str:
    """
    Pin and resolve a deterministic rulepack version.

    If a specific version is requested and supported, return it; otherwise fallback
    to DEFAULT_RULEPACK_VERSION. This keeps execution deterministic per job.
    """
    # TODO: verify against available rulepack files under rules/ if needed.
    return requested_version or DEFAULT_RULEPACK_VERSION

