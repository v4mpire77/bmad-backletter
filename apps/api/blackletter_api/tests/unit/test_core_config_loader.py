from __future__ import annotations

from pathlib import Path

from blackletter_api.core_config_loader import CoreConfig, load_core_config


def test_load_core_config_defaults_when_missing(tmp_path: Path) -> None:
    cfg_path = tmp_path / "missing.yaml"
    cfg = load_core_config(str(cfg_path))
    assert cfg == CoreConfig()


def test_load_core_config_from_file(tmp_path: Path) -> None:
    cfg_path = tmp_path / "core-config.yaml"
    cfg_path.write_text("evidence_window_sentences: 5\nenable_weak_language: false\n", encoding="utf-8")
    cfg = load_core_config(str(cfg_path))
    assert cfg.evidence_window_sentences == 5
    assert cfg.enable_weak_language is False


def test_load_core_config_malformed_yaml_returns_defaults(tmp_path: Path) -> None:
    cfg_path = tmp_path / "core-config.yaml"
    cfg_path.write_text("::bad_yaml::", encoding="utf-8")
    cfg = load_core_config(str(cfg_path))
    assert cfg == CoreConfig()


def test_load_core_config_uses_default_path(monkeypatch, tmp_path: Path) -> None:
    cfg_path = tmp_path / "core-config.yaml"
    cfg_path.write_text("evidence_window_sentences: 7\nenable_weak_language: true\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    cfg = load_core_config()
    assert cfg.evidence_window_sentences == 7
    assert cfg.enable_weak_language is True
