from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def test_list_analyses_empty():
    res = client.get("/api/analyses?limit=50")
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    assert body == []

