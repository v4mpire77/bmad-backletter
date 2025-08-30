from __future__ import annotations

import logging
from pathlib import Path

import pytest
import yaml

from blackletter_api.core_config_loader import CoreConfig, load_core_config


def test_load_core_config_logs_and_defaults_on_bad_yaml(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    cfg_file = tmp_path / "core-config.yaml"
    cfg_file.write_text("invalid: [\n")
    with caplog.at_level(logging.WARNING):
        cfg = load_core_config(str(cfg_file))
    assert cfg == CoreConfig()
    assert any("Failed to load core config" in record.message for record in caplog.records)


def test_load_core_config_raises_when_required_and_missing(tmp_path: Path) -> None:
    missing_file = tmp_path / "nope.yaml"
    with pytest.raises(FileNotFoundError):
        load_core_config(str(missing_file), required=True)


def test_load_core_config_raises_when_required_on_error(tmp_path: Path) -> None:
    cfg_file = tmp_path / "core-config.yaml"
    cfg_file.write_text("evidence_window_sentences: [1, 2\n")
    with pytest.raises(yaml.YAMLError):
        load_core_config(str(cfg_file), required=True)
