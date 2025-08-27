from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml


@dataclass
class CoreConfig:
    evidence_window_sentences: int = 2
    enable_weak_language: bool = True


def load_core_config(path: str | None = None) -> CoreConfig:
    cfg_path = Path(path) if path else Path.cwd() / "core-config.yaml"
    if not cfg_path.exists():
        # Return defaults if missing; upstream can log a warning.
        return CoreConfig()

    try:
        data: Dict[str, Any] = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        return CoreConfig(
            evidence_window_sentences=int(data.get("evidence_window_sentences", 2)),
            enable_weak_language=bool(data.get("enable_weak_language", True)),
        )
    except Exception as exc:  # noqa: BLE001
        # On malformed config, fall back to defaults — detection should still run.
        return CoreConfig()
