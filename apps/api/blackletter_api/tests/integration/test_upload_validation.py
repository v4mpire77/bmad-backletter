from __future__ import annotations

from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.routers.uploads import MAX_UPLOAD_BYTES


client = TestClient(app)


def test_rejects_unsupported_mime():
    files = {"file": ("image.png", b"abcd", "image/png")}
    resp = client.post("/api/uploads", files=files)
    assert resp.status_code == 400
    assert resp.json()["detail"] == "unsupported mime type"


def test_rejects_oversized_upload():
    # Create a payload just over the limit
    payload = b"x" * (MAX_UPLOAD_BYTES + 1)
    files = {"file": ("big.txt", payload, "text/plain")}
    resp = client.post("/api/uploads", files=files)
    assert resp.status_code == 413
    assert resp.json()["detail"] == "file too large"

