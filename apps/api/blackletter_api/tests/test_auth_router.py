import pytest
from fastapi.testclient import TestClient
from apps.api.blackletter_api.main import app
from apps.api.blackletter_api import database
from apps.api.blackletter_api.models import auth as auth_models


@pytest.fixture
def client(db_session_mock):
    app.dependency_overrides[database.get_db] = lambda: db_session_mock
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def clear_users(db_session_mock):
    db_session_mock.query(auth_models.User).delete()
    db_session_mock.commit()

def test_auth_routes_registered(client):
    # Check register endpoint exists and returns 422 for missing body
    resp = client.post('/api/v1/auth/register', json={})
    assert resp.status_code in (400, 422)

    # Check login endpoint exists (missing body -> 422)
    resp = client.post('/api/v1/auth/login', json={})
    assert resp.status_code in (400, 422)


def test_register_user_success(client):
    payload = {"email": "user@example.com", "password": "secret", "name": "User"}
    resp = client.post('/api/v1/auth/register', json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]
    assert "id" in data


def test_register_user_duplicate_email(client):
    payload = {"email": "user@example.com", "password": "secret", "name": "User"}
    client.post('/api/v1/auth/register', json=payload)
    resp = client.post('/api/v1/auth/register', json=payload)
    assert resp.status_code == 409
    assert resp.json()["detail"] == "Email already registered"
