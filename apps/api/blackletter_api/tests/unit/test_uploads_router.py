from __future__ import annotations

from io import BytesIO

from fastapi.testclient import TestClient

from blackletter_api.main import app

client = TestClient(app)


def test_upload_rejects_large_file(monkeypatch) -> None:
    def _raise(*args, **kwargs):  # type: ignore[unused-arg]
        raise ValueError("file_too_large")

    monkeypatch.setattr(
        "blackletter_api.routers.contracts.storage.save_upload", _raise
    )
    files = {"file": ("doc.pdf", BytesIO(b"data"), "application/pdf")}
    resp = client.post("/api/contracts", files=files)
    assert resp.status_code == 413
    assert resp.json() == {"detail": "file_too_large"}


def test_upload_rejects_unsupported_type() -> None:
    files = {"file": ("doc.txt", BytesIO(b"data"), "text/plain")}
    resp = client.post("/api/contracts", files=files)
    assert resp.status_code == 415
    assert resp.json() == {"detail": "unsupported_file_type"}


def test_upload_success(monkeypatch) -> None:
    def _save(file, dest, max_bytes=10 * 1024 * 1024):  # type: ignore[unused-arg]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b"hello")
        return 5

    monkeypatch.setattr(
        "blackletter_api.routers.contracts.storage.save_upload", _save
    )
    monkeypatch.setattr(
        "blackletter_api.routers.contracts.new_job", lambda analysis_id: "job1"
    )
    monkeypatch.setattr(
        "blackletter_api.routers.contracts.process_job", lambda *args, **kwargs: None
    )

    files = {"file": ("doc.pdf", BytesIO(b"%PDF"), "application/pdf")}
    resp = client.post("/api/contracts", files=files)
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "queued"
    assert data["job_id"] == "job1"
    assert data["analysis_id"]
