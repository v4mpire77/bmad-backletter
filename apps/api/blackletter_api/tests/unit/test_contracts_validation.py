from __future__ import annotations

from io import BytesIO

import pytest
from fastapi.testclient import TestClient

from blackletter_api.main import app


client = TestClient(app)


def _post_upload(filename: str, content_type: str, data: bytes):
    files = {"file": (filename, BytesIO(data), content_type)}
    return client.post("/api/contracts", files=files)


def test_upload_missing_file():
    res = client.post("/api/contracts", files={})
    assert res.status_code == 422  # FastAPI validation


@pytest.mark.parametrize(
    "name,ctype",
    [
        ("foo.txt", "text/plain"),
        ("image.png", "image/png"),
    ],
)
def test_upload_unsupported_type(name: str, ctype: str):
    res = _post_upload(name, ctype, b"hello")
    assert res.status_code == 415
    body = res.json()
    assert body["code"] == "unsupported_file_type"
    assert isinstance(body["message"], str)


def test_upload_too_large_triggers_413():
    big = b"x" * (10 * 1024 * 1024 + 1)
    res = _post_upload("big.pdf", "application/pdf", big)
    assert res.status_code == 413
    body = res.json()
    assert body["code"] == "file_too_large"
    assert isinstance(body["message"], str)


def test_contract_validation_status_schema():
    res = client.get("/api/contracts/validation-status/job123")
    assert res.status_code == 200
    data = res.json()
    assert data["job_id"] == "job123"
    assert data["validation_results"]["gdpr_compliance"] == "pass"

