from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import logging
import yaml


logger = logging.getLogger(__name__)


@dataclass
class CoreConfig:
    evidence_window_sentences: int = 2
    enable_weak_language: bool = True


def load_core_config(path: str | None = None, *, required: bool = False) -> CoreConfig:
    cfg_path = Path(path) if path else Path.cwd() / "core-config.yaml"
    if not cfg_path.exists():
        logger.warning("Core config file %s not found. Using defaults.", cfg_path)
        if required:
            raise FileNotFoundError(f"Core config file not found: {cfg_path}")
        return CoreConfig()

    try:
        data: Dict[str, Any] = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        return CoreConfig(
            evidence_window_sentences=int(data.get("evidence_window_sentences", 2)),
            enable_weak_language=bool(data.get("enable_weak_language", True)),
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to load core config from %s: %s", cfg_path, exc)
        if required:
            raise
        # On malformed config, fall back to defaults — detection should still run.
        return CoreConfig()
