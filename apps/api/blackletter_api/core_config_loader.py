from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Literal

import logging
import yaml


@dataclass
class LLMConfig:
    provider: Literal["none", "openai", "anthropic", "gemini"] = "none"
    gate_policy: str = "snippet_only"
    snippet_max_tokens: int = 220


@dataclass
class BudgetConfig:
    hard_cap_tokens_per_doc: int = 1500
    on_exceed: str = "needs_review"


@dataclass
class CacheConfig:
    kind: str = "sqlite"
    key: list[str] = None

    def __post_init__(self):
        if self.key is None:
            self.key = ["prompt_id", "snippet_hash"]


@dataclass
class OCRConfig:
    enabled: bool = False


@dataclass
class SecurityConfig:
    redact_pii: bool = True


@dataclass
class CoreConfig:
    evidence_window_sentences: int = 2
    enable_weak_language: bool = True
    llm: LLMConfig = None
    budget: BudgetConfig = None
    cache: CacheConfig = None
    ocr: OCRConfig = None
    security: SecurityConfig = None

    def __post_init__(self):
        if self.llm is None:
            self.llm = LLMConfig()
        if self.budget is None:
            self.budget = BudgetConfig()
        if self.cache is None:
            self.cache = CacheConfig()
        if self.ocr is None:
            self.ocr = OCRConfig()
        if self.security is None:
            self.security = SecurityConfig()


def load_core_config(path: str | None = None) -> CoreConfig:
    cfg_path = Path(path) if path else Path.cwd() / "core-config.yaml"
    if not cfg_path.exists():
        # Return defaults if missing; upstream can log a warning.
        return CoreConfig()

    try:
        data: Dict[str, Any] = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        
        # Load nested configurations
        llm_data = data.get("llm", {})
        llm_config = LLMConfig(
            provider=llm_data.get("provider", "none"),
            gate_policy=llm_data.get("gate_policy", "snippet_only"),
            snippet_max_tokens=int(llm_data.get("snippet_max_tokens", 220))
        )
        
        budget_data = data.get("budget", {})
        budget_config = BudgetConfig(
            hard_cap_tokens_per_doc=int(budget_data.get("hard_cap_tokens_per_doc", 1500)),
            on_exceed=budget_data.get("on_exceed", "needs_review")
        )
        
        cache_data = data.get("cache", {})
        cache_config = CacheConfig(
            kind=cache_data.get("kind", "sqlite"),
            key=cache_data.get("key", ["prompt_id", "snippet_hash"])
        )
        
        ocr_data = data.get("ocr", {})
        ocr_config = OCRConfig(
            enabled=bool(ocr_data.get("enabled", False))
        )
        
        security_data = data.get("security", {})
        security_config = SecurityConfig(
            redact_pii=bool(security_data.get("redact_pii", True))
        )
        
        return CoreConfig(
            evidence_window_sentences=int(data.get("evidence_window_sentences", 2)),
            enable_weak_language=bool(data.get("enable_weak_language", True)),
            llm=llm_config,
            budget=budget_config,
            cache=cache_config,
            ocr=ocr_config,
            security=security_config,
        )
    except Exception as exc:  # noqa: BLE001
        # On malformed config, log the error and fall back to defaults
        logging.warning("Failed to load core config: %s", exc)
        return CoreConfig()
