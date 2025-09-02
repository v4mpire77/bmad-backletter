from __future__ import annotations

import os
import json
import threading
import time
from pathlib import Path
from typing import Dict, Optional, Any, Tuple
from dataclasses import dataclass, asdict

@dataclass
class TokenUsage:
    """Tracks token usage for a single analysis."""
    analysis_id: str
    total_tokens: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost: float = 0.0
    last_updated: float = 0.0
    cap_exceeded: bool = False
    cap_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenUsage":
        return cls(**data)

    def add_tokens(self, input_tokens: int, output_tokens: int, cost_per_token: float = 0.0001) -> None:
        """Add token usage and update totals."""
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.total_tokens = self.input_tokens + self.output_tokens
        self.estimated_cost += (input_tokens + output_tokens) * cost_per_token
        self.last_updated = time.time()


class TokenLedger:
    """Thread-safe token usage tracker with persistence."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path("data/analyses")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._cache: Dict[str, TokenUsage] = {}
        self._cap_limit = int(os.getenv("TOKEN_CAP_PER_DOC", "20000"))
        self._cost_per_token = float(os.getenv("TOKEN_COST_PER_UNIT", "0.0001"))

    def _get_usage_path(self, analysis_id: str) -> Path:
        """Get the path for token usage data."""
        return self.data_dir / analysis_id / "tokens.json"

    def _load_usage(self, analysis_id: str) -> TokenUsage:
        """Load token usage from disk or create new."""
        if analysis_id in self._cache:
            return self._cache[analysis_id]

        usage_path = self._get_usage_path(analysis_id)
        if usage_path.exists():
            try:
                with usage_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                usage = TokenUsage.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                usage = TokenUsage(analysis_id=analysis_id)
        else:
            usage = TokenUsage(analysis_id=analysis_id)

        self._cache[analysis_id] = usage
        return usage

    def _save_usage(self, usage: TokenUsage) -> None:
        """Save token usage to disk."""
        usage_path = self._get_usage_path(usage.analysis_id)
        usage_path.parent.mkdir(parents=True, exist_ok=True)

        with usage_path.open("w", encoding="utf-8") as f:
            json.dump(usage.to_dict(), f, indent=2)

    def add_tokens(
        self,
        analysis_id: str,
        input_tokens: int,
        output_tokens: int
    ) -> Tuple[bool, Optional[str]]:
        """Add token usage for an analysis.

        Returns (cap_exceeded: bool, reason: Optional[str])
        """
        with self._lock:
            usage = self._load_usage(analysis_id)

            # Check cap before adding tokens
            projected_total = usage.total_tokens + input_tokens + output_tokens
            if projected_total > self._cap_limit:
                reason = f"Token cap exceeded: {projected_total}/{self._cap_limit} tokens"
                usage.cap_exceeded = True
                usage.cap_reason = reason
                self._save_usage(usage)
                return True, reason

            # Add tokens and save
            usage.add_tokens(input_tokens, output_tokens, self._cost_per_token)
            self._save_usage(usage)

            return False, None

    def get_usage(self, analysis_id: str) -> TokenUsage:
        """Get current token usage for an analysis."""
        with self._lock:
            return self._load_usage(analysis_id)

    def get_all_usage(self) -> Dict[str, TokenUsage]:
        """Get all token usage records."""
        with self._lock:
            # Load all existing records
            all_usage = {}
            if self.data_dir.exists():
                for analysis_dir in self.data_dir.iterdir():
                    if analysis_dir.is_dir():
                        analysis_id = analysis_dir.name
                        all_usage[analysis_id] = self._load_usage(analysis_id)

            return all_usage

    def get_cap_limit(self) -> int:
        """Get the current token cap limit."""
        return self._cap_limit

    def set_cap_limit(self, limit: int) -> None:
        """Set the token cap limit."""
        with self._lock:
            self._cap_limit = limit

    def get_total_metrics(self) -> Dict[str, Any]:
        """Get aggregate metrics across all analyses."""
        with self._lock:
            all_usage = self.get_all_usage()

            total_tokens = sum(u.total_tokens for u in all_usage.values())
            total_cost = sum(u.estimated_cost for u in all_usage.values())
            cap_exceeded_count = sum(1 for u in all_usage.values() if u.cap_exceeded)
            analysis_count = len(all_usage)

            return {
                "total_analyses": analysis_count,
                "total_tokens": total_tokens,
                "total_cost": round(total_cost, 4),
                "cap_exceeded_count": cap_exceeded_count,
                "cap_limit": self._cap_limit,
                "average_tokens_per_analysis": round(total_tokens / max(analysis_count, 1), 2),
                "cap_exceeded_percentage": round((cap_exceeded_count / max(analysis_count, 1)) * 100, 2)
            }

    def reset_usage(self, analysis_id: str) -> None:
        """Reset token usage for an analysis."""
        with self._lock:
            if analysis_id in self._cache:
                del self._cache[analysis_id]

            usage_path = self._get_usage_path(analysis_id)
            if usage_path.exists():
                usage_path.unlink()


# Global ledger instance
_ledger_instance: Optional[TokenLedger] = None
_ledger_lock = threading.Lock()


def get_token_ledger() -> TokenLedger:
    """Get the global token ledger instance."""
    global _ledger_instance
    if _ledger_instance is None:
        with _ledger_lock:
            if _ledger_instance is None:
                # Try to use the same data directory as analysis storage
                from .storage import get_data_dir
                data_dir = get_data_dir()
                _ledger_instance = TokenLedger(data_dir / "analyses")
    return _ledger_instance


def token_capping_enabled() -> bool:
    """Check if token capping is enabled."""
    return os.getenv("TOKEN_CAPPING_ENABLED", "1") == "1"


def should_apply_token_capping() -> bool:
    """Check if token capping should be applied (enabled and LLM features active)."""
    return token_capping_enabled() and os.getenv("LLM_ENABLED", "0") == "1"
