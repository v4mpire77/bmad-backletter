from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from blackletter_api.routers.admin import router as admin_router
from blackletter_api.services.rulepack_loader import RulepackError

app = FastAPI()
app.include_router(admin_router)
client = TestClient(app)


def test_list_rulepacks_returns_metadata(monkeypatch) -> None:
    def _fake() -> list[dict[str, str]]:
        return [
            {
                "id": "pack1",
                "version": "1.0",
                "author": "tester",
                "created_at": "2024-01-01",
            }
        ]

    monkeypatch.setattr(
        "blackletter_api.routers.admin.list_rulepack_metadata", _fake
    )
    res = client.get("/api/admin/rulepacks", headers={"X-User-Role": "admin"})
    assert res.status_code == 200
    assert res.json() == _fake()


def test_list_rulepacks_handles_error(monkeypatch) -> None:
    def _raise() -> list[dict[str, str]]:
        raise RulepackError("not found")

    monkeypatch.setattr(
        "blackletter_api.routers.admin.list_rulepack_metadata", _raise
    )
    res = client.get("/api/admin/rulepacks", headers={"X-User-Role": "admin"})
    assert res.status_code == 404
    assert res.json()["detail"] == "not found"
