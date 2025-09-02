import importlib
from pathlib import Path

import pytest
import sqlalchemy

from blackletter_api import config, database
from blackletter_api.models import entities


def _reload_database(monkeypatch: pytest.MonkeyPatch, url: str) -> dict:
    called: dict = {}

    def fake_create_engine(url_arg: str, **kwargs):
        called["url"] = url_arg
        called["kwargs"] = kwargs

        class DummyEngine:
            pass

        return DummyEngine()

    monkeypatch.setattr(sqlalchemy, "create_engine", fake_create_engine)
    monkeypatch.setattr(config, "settings", config.Settings(database_url=url))
    importlib.reload(database)
    return called


@pytest.fixture(autouse=True)
def restore_database() -> None:
    original_settings = config.settings
    yield
    config.settings = original_settings
    importlib.reload(database)
    db_path = Path(__file__).resolve().parents[3] / "test.db"
    real_engine = sqlalchemy.create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    database.engine = real_engine
    database.SessionLocal.configure(bind=real_engine)
    entities.Base.metadata.create_all(bind=real_engine)


def test_engine_creation_sqlite(monkeypatch: pytest.MonkeyPatch) -> None:
    info = _reload_database(monkeypatch, "sqlite:///:memory:")
    assert info["kwargs"]["connect_args"] == {"check_same_thread": False}
    assert info["url"] == "sqlite:///:memory:"


def test_engine_creation_postgres(monkeypatch: pytest.MonkeyPatch) -> None:
    info = _reload_database(
        monkeypatch, "postgresql://user:pass@localhost/db"
    )
    assert "connect_args" not in info["kwargs"]
    assert info["url"] == "postgresql://user:pass@localhost/db"
