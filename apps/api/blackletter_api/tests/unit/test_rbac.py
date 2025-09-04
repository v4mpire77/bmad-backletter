from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from apps.api.dependencies.auth import require_role
from apps.api.models.user import Role

app = FastAPI()


@app.get("/admin", dependencies=[Depends(require_role(Role.ADMIN))])
async def admin_only_endpoint():
    return {"message": "ok"}


def get_client() -> TestClient:
    return TestClient(app)


def test_admin_can_access():
    client = get_client()
    response = client.get("/admin", headers={"X-User-Role": "admin"})
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}


def test_reviewer_forbidden():
    client = get_client()
    response = client.get("/admin", headers={"X-User-Role": "reviewer"})
    assert response.status_code == 403
