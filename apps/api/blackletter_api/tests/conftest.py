import os
import sys
from pathlib import Path

import pytest

# Ensure `apps/api` is on sys.path so `import blackletter_api` works
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# Ensure AUTH_PEPPER is available for tests
os.environ.setdefault("AUTH_PEPPER", "test-pepper")

@pytest.fixture(autouse=True)
def auth_pepper_env(monkeypatch) -> None:
    """Provide a default AUTH_PEPPER for tests via environment."""
    monkeypatch.setenv("AUTH_PEPPER", "test-pepper")

from sqlalchemy import create_engine

from blackletter_api import database
from blackletter_api.models import entities

# Rebind engine to a known absolute path and ensure tables exist
db_path = Path(__file__).resolve().parents[3] / "test.db"
database.engine = create_engine(
    f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
)
database.SessionLocal.configure(bind=database.engine)
entities.Base.metadata.create_all(bind=database.engine)

