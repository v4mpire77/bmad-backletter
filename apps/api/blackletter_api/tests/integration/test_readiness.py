from fastapi import APIRouter
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from blackletter_api import database
from blackletter_api.routers import rules

# Ensure main import succeeds even if rules router is not implemented
rules.router = APIRouter()
from blackletter_api.main import app

client = TestClient(app)


def test_readiness_db_failure(monkeypatch):
    """Return 503 when the database query fails."""

    def fail_connect(*args, **kwargs):
        raise SQLAlchemyError("boom")

    monkeypatch.setattr(database.engine, "connect", fail_connect)

    resp = client.get("/readyz")
    assert resp.status_code == 503
    assert resp.json() == {"ok": False, "db": "error"}
