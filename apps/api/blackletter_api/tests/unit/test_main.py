from __future__ import annotations

from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def test_read_root() -> None:
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_healthz() -> None:
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json() == {"ok": True}
