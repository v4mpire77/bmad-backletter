from fastapi.testclient import TestClient
from apps.api.blackletter_api.main import app

client = TestClient(app)

def test_auth_routes_registered():
    # Check register endpoint exists and returns 422 for missing body
    resp = client.post('/api/v1/auth/register', json={})
    assert resp.status_code in (400, 422)

    # Check login endpoint exists (missing body -> 422)
    resp = client.post('/api/v1/auth/login', json={})
    assert resp.status_code in (400, 422)
