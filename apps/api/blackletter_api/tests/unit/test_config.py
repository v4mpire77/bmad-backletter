from __future__ import annotations

import importlib
import pytest
from pydantic import ValidationError


def test_settings_requires_secret_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SECRET_KEY", "test")
    config = importlib.import_module("blackletter_api.config")
    monkeypatch.delenv("SECRET_KEY", raising=False)
    with pytest.raises(ValidationError):
        config.Settings()
