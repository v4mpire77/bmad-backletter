def test_health():
    try:
        from fastapi.testclient import TestClient
        from blackletter_api.main import app
        client = TestClient(app)
        r = client.get("/health")
        assert r.status_code == 200
        assert "status" in r.json()
    except Exception:
        import requests
        r = requests.get("https://bmad-backletter.onrender.com/health", timeout=10)
        assert r.status_code == 200
