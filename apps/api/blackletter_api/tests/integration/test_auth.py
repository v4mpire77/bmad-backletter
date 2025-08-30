"""Integration tests for authentication endpoints."""
from fastapi.testclient import TestClient
from fastapi import FastAPI

from apps.api.blackletter_api.routers import auth

app = FastAPI()
app.include_router(auth.router)
client = TestClient(app)


def test_login_success() -> None:
    response = client.post(
        "/api/auth/login",
        json={"username": "user@example.com", "password": "strongPassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data and data["access_token"]


def test_login_failure() -> None:
    response = client.post(
        "/api/auth/login",
        json={"username": "user@example.com", "password": "bad"},
    )
    assert response.status_code == 401
