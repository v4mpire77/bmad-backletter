import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import uuid

# ensure required settings for database
os.environ.setdefault("SECRET_KEY", "test-secret")

from blackletter_api import database
from blackletter_api.models.entities import Report
from blackletter_api.routers.reports import router as reports_router

app = FastAPI()
app.include_router(reports_router, prefix="/api")


@pytest.fixture
def client(db_session_mock):
    app.dependency_overrides[database.get_db] = lambda: db_session_mock
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def clear_reports(db_session_mock):
    db_session_mock.query(Report).delete()
    db_session_mock.commit()


def test_list_reports_initially_empty(client):
    res = client.get("/api/reports")
    assert res.status_code == 200
    assert res.json() == []


def test_create_report_and_list(client, db_session_mock):
    payload = {"include_logo": True, "include_meta": False, "date_format": "MDY"}
    res = client.post("/api/reports/test123", json=payload)
    assert res.status_code == 201
    data = res.json()
    for key in ["id", "analysis_id", "filename", "created_at", "options"]:
        assert key in data
    assert data["analysis_id"] == "test123"
    # ensure report persisted to the database
    report = db_session_mock.query(Report).filter_by(id=uuid.UUID(data["id"])).first()
    assert report is not None
    assert report.analysis_id == "test123"
    # list reports now contains the created record
    res2 = client.get("/api/reports")
    assert res2.status_code == 200
    items = res2.json()
    assert any(r["id"] == data["id"] for r in items)
