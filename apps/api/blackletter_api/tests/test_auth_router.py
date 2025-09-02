import pytest
from fastapi.testclient import TestClient
from apps.api.blackletter_api.main import app
from apps.api.blackletter_api import database
from apps.api.blackletter_api.models import auth as auth_models

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_users():
    db = database.SessionLocal()
    db.query(auth_models.User).delete()
    db.commit()
    db.close()

def test_auth_routes_registered():
    # Check register endpoint exists and returns 422 for missing body
    resp = client.post('/api/v1/auth/register', json={})
    assert resp.status_code in (400, 422)

    # Check login endpoint exists (missing body -> 422)
    resp = client.post('/api/v1/auth/login', json={})
    assert resp.status_code in (400, 422)


def test_register_user_success():
    payload = {"email": "user@example.com", "password": "secret", "name": "User"}
    resp = client.post('/api/v1/auth/register', json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]
    assert "id" in data


def test_register_user_duplicate_email():
    payload = {"email": "user@example.com", "password": "secret", "name": "User"}
    client.post('/api/v1/auth/register', json=payload)
    resp = client.post('/api/v1/auth/register', json=payload)
    assert resp.status_code == 409
    assert resp.json()["detail"] == "Email already registered"
