from __future__ import annotations

from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def test_login_returns_token() -> None:
    res = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "password"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["access_token"] == "fake-token"
    assert data["token_type"] == "bearer"


def test_login_rejects_invalid_credentials() -> None:
    res = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert res.status_code == 401
    assert res.json()["detail"] == "invalid_credentials"
