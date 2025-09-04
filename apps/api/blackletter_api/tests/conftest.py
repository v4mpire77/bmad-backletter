import os
import sys
from pathlib import Path

import pytest

# Ensure `apps/api` is on sys.path so `import blackletter_api` works
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# Ensure required secrets are available for tests
os.environ.setdefault("AUTH_PEPPER", "test-pepper")
os.environ.setdefault("SECRET_KEY", "test-secret")


@pytest.fixture(autouse=True)
def auth_pepper_env(monkeypatch) -> None:
    """Provide default secret values for tests via environment."""
    monkeypatch.setenv("AUTH_PEPPER", "test-pepper")
    monkeypatch.setenv("SECRET_KEY", "test-secret")

from sqlalchemy import create_engine

from blackletter_api import database
from blackletter_api.models import entities, auth as auth_models, organization as organization_models  # noqa: F401

# Rebind engine to a known absolute path and ensure tables exist
db_path = Path(__file__).resolve().parents[3] / "test.db"
database.engine = create_engine(
    f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
)
database.SessionLocal.configure(bind=database.engine)
database.Base.metadata.create_all(bind=database.engine)


# Enable Celery eager mode for deterministic tests (run tasks synchronously)
try:
    from blackletter_api.services import tasks as _tasks_service
    _tasks_service.celery_app.conf.task_always_eager = True
    _tasks_service.celery_app.conf.task_eager_propagates = True
except Exception:  # pragma: no cover - do not fail tests if unavailable
    pass

# Stub Redis client for tests to avoid external dependency
class DummyRedis:
    def __init__(self):
        self.store = {}
    def hset(self, key, mapping):
        self.store[key] = mapping
    def hgetall(self, key):
        return self.store.get(key, {})
    def exists(self, key):
        return key in self.store

try:
    from blackletter_api.services import tasks as _tasks_service
    _tasks_service.redis_client = DummyRedis()
except Exception:  # pragma: no cover
    pass
