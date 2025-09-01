"""Simple in-memory analytics tracking utilities."""

from __future__ import annotations

from collections import defaultdict
from threading import Lock
from typing import DefaultDict, Dict


class AnalyticsTracker:
    """Tracks counts of named events in a thread-safe manner."""

    def __init__(self) -> None:
        self._counts: DefaultDict[str, int] = defaultdict(int)
        self._lock = Lock()

    def record(self, event: str) -> None:
        """Increment the counter for ``event``."""

        with self._lock:
            self._counts[event] += 1

    def snapshot(self) -> Dict[str, int]:
        """Return a shallow copy of all counters."""

        with self._lock:
            return dict(self._counts)


# A module-level tracker used by the FastAPI endpoints.
tracker = AnalyticsTracker()


__all__ = ["AnalyticsTracker", "tracker"]
