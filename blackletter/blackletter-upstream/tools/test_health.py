from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

resp = client.get('/health')
print('status_code=', resp.status_code)
print('json=', resp.json())
