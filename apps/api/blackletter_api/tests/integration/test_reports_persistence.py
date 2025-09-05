import os
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import uuid

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


def test_create_report_persists_to_db(client, db_session_mock):
    # ensure table clean
    db_session_mock.query(Report).delete()
    db_session_mock.commit()

    payload = {"include_logo": False, "include_meta": True, "date_format": "ISO"}
    res = client.post("/api/reports/sample", json=payload)
    assert res.status_code == 201
    data = res.json()

    report = db_session_mock.query(Report).filter_by(id=uuid.UUID(data["id"])).first()
    assert report is not None
    assert report.analysis_id == "sample"
    assert report.options["date_format"] == "ISO"
