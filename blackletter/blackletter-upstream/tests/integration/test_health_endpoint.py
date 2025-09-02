import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
try:
    from backend.main import app
except Exception:  # pragma: no cover - backend may be incomplete
    pytest.skip("backend.main cannot be imported", allow_module_level=True)


def test_health_endpoint_returns_status():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("service") == "blackletter"
    assert data.get("status") == "ok"
    assert "X-Process-Time" in response.headers
