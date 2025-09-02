import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import uuid

# ensure required settings for database
os.environ.setdefault("SECRET_KEY", "test-secret")

from blackletter_api import database
from blackletter_api.models.entities import Analysis, Report
from blackletter_api.routers.reports import router as reports_router

app = FastAPI()
app.include_router(reports_router, prefix="/api")

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_reports():
    db = database.SessionLocal()
    try:
        db.query(Report).delete()
        db.query(Analysis).delete()
        db.commit()
    finally:
        db.close()


def test_list_reports_initially_empty():
    res = client.get("/api/reports")
    assert res.status_code == 200
    assert res.json() == []


def test_create_report_and_list():
    payload = {"include_logo": True, "include_meta": False, "date_format": "MDY"}
    analysis_id = uuid.uuid4()
    db = database.SessionLocal()
    try:
        analysis = Analysis(
            id=analysis_id,
            filename="file.txt",
            size_bytes=123,
            mime_type="text/plain",
        )
        db.add(analysis)
        db.commit()
    finally:
        db.close()

    res = client.post(f"/api/reports/{analysis_id}", json=payload)
    assert res.status_code == 201
    data = res.json()
    for key in ["id", "analysis_id", "filename", "file_path", "created_at", "options"]:
        assert key in data
    assert data["analysis_id"] == str(analysis_id)
    # ensure report persisted to the database
    db = database.SessionLocal()
    try:
        report = db.query(Report).filter_by(id=uuid.UUID(data["id"])).first()
        assert report is not None
        assert report.analysis_id == str(analysis_id)
        assert report.file_path
    finally:
        db.close()
    # list reports now contains the created record
    res2 = client.get("/api/reports")
    assert res2.status_code == 200
    items = res2.json()
    assert any(r["id"] == data["id"] for r in items)
