import os
from fastapi import FastAPI
from fastapi.testclient import TestClient
import uuid

os.environ.setdefault("SECRET_KEY", "test-secret")

from blackletter_api import database
from blackletter_api.models.entities import Report
from blackletter_api.routers.reports import router as reports_router

app = FastAPI()
app.include_router(reports_router, prefix="/api")

client = TestClient(app)


def test_create_report_persists_to_db():
    # ensure table clean
    db = database.SessionLocal()
    try:
        db.query(Report).delete()
        db.commit()
    finally:
        db.close()

    payload = {"include_logo": False, "include_meta": True, "date_format": "ISO"}
    res = client.post("/api/reports/sample", json=payload)
    assert res.status_code == 201
    data = res.json()

    db = database.SessionLocal()
    try:
        report = db.query(Report).filter_by(id=uuid.UUID(data["id"])).first()
        assert report is not None
        assert report.analysis_id == "sample"
        assert report.options["date_format"] == "ISO"
    finally:
        db.close()
