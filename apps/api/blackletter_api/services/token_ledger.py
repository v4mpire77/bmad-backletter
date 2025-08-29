from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Optional

from .storage import analysis_dir


_locks: Dict[str, threading.Lock] = {}
_global_lock = threading.Lock()


def _get_lock(analysis_id: str) -> threading.Lock:
    with _global_lock:
        if analysis_id not in _locks:
            _locks[analysis_id] = threading.Lock()
        return _locks[analysis_id]


def get_cap_per_doc() -> int:
    try:
        return int(os.getenv("TOKEN_CAP_PER_DOC", "20000"))
    except ValueError:
        return 20000


def llm_provider_enabled() -> bool:
    # Provider is OFF by default per story requirements
    return os.getenv("LLM_PROVIDER_ENABLED", "0") == "1"


@dataclass
class Ledger:
    analysis_id: str
    total_tokens: int = 0
    cap_per_doc: int = 20000
    needs_review: bool = False
    reason: Optional[str] = None

    @staticmethod
    def path_for(analysis_id: str) -> Path:
        return analysis_dir(analysis_id) / "tokens.json"

    @staticmethod
    def load(analysis_id: str) -> "Ledger":
        p = Ledger.path_for(analysis_id)
        if not p.exists():
            return Ledger(analysis_id=analysis_id, cap_per_doc=get_cap_per_doc())
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            return Ledger(
                analysis_id=analysis_id,
                total_tokens=int(data.get("total_tokens", 0)),
                cap_per_doc=int(data.get("cap_per_doc", get_cap_per_doc())),
                needs_review=bool(data.get("needs_review", False)),
                reason=data.get("reason"),
            )
        except Exception:
            # If corrupted, reset to defaults rather than failing pipeline
            return Ledger(analysis_id=analysis_id, cap_per_doc=get_cap_per_doc())

    def save(self) -> None:
        p = Ledger.path_for(self.analysis_id)
        # Ensure parent directory exists before writing
        p.parent.mkdir(parents=True, exist_ok=True)
        data = json.dumps(asdict(self), indent=2)
        p.write_text(data, encoding="utf-8")

        # Also ensure write to the canonical storage path used by other modules/tests
        try:
            from . import storage as _storage

            canonical_path = _storage.analysis_dir(self.analysis_id) / "tokens.json"
            if canonical_path != p:
                canonical_path.parent.mkdir(parents=True, exist_ok=True)
                canonical_path.write_text(data, encoding="utf-8")
        except Exception:
            # Do not fail save() if mirror write fails; primary path already persisted
            pass


def add_tokens(analysis_id: str, tokens: int) -> Ledger:
    if tokens <= 0:
        return get_ledger(analysis_id)

    lock = _get_lock(analysis_id)
    with lock:
        ledger = Ledger.load(analysis_id)
        ledger.cap_per_doc = get_cap_per_doc()
        ledger.total_tokens += tokens
        if not ledger.needs_review and ledger.total_tokens >= ledger.cap_per_doc:
            ledger.needs_review = True
            ledger.reason = (
                f"token_cap_exceeded: {ledger.total_tokens} >= {ledger.cap_per_doc}"
            )
        ledger.save()
        return ledger


def get_ledger(analysis_id: str) -> Ledger:
    # Non-mutating read
    return Ledger.load(analysis_id)


def mark_needs_review(analysis_id: str, reason: str) -> Ledger:
    lock = _get_lock(analysis_id)
    with lock:
        ledger = Ledger.load(analysis_id)
        ledger.needs_review = True
        ledger.reason = reason
        ledger.save()
        return ledger


def reset_ledger(analysis_id: str) -> None:
    lock = _get_lock(analysis_id)
    with lock:
        ledger = Ledger(analysis_id=analysis_id, cap_per_doc=get_cap_per_doc())
        ledger.save()


def list_all_ledgers() -> Dict[str, Ledger]:
    # Scan .data/analyses/*/tokens.json
    root = Path(".data") / "analyses"
    results: Dict[str, Ledger] = {}
    if not root.exists():
        return results
    for analysis_dir_path in root.iterdir():
        if not analysis_dir_path.is_dir():
            continue
        analysis_id = analysis_dir_path.name
        p = analysis_dir_path / "tokens.json"
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                results[analysis_id] = Ledger(
                    analysis_id=analysis_id,
                    total_tokens=int(data.get("total_tokens", 0)),
                    cap_per_doc=int(data.get("cap_per_doc", get_cap_per_doc())),
                    needs_review=bool(data.get("needs_review", False)),
                    reason=data.get("reason"),
                )
            except Exception:
                # Skip malformed files
                continue
    return results


