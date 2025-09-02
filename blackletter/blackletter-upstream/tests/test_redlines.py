import os
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure src/backend is importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from backend.database import Base, get_db  # noqa: E402
from backend.models.redline import Redline  # noqa: E402
from backend.routers.redlines import router  # noqa: E402


def test_save_redline_persists_record():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    payload = {"issueId": "ISS-123", "text": "Need to update clause."}
    response = client.post("/redlines", json=payload)
    assert response.status_code == 200
    redline_id = response.json()["id"]

    with TestingSessionLocal() as session:
        saved = session.get(Redline, redline_id)
        assert saved is not None
        assert saved.issue_id == payload["issueId"]
        assert saved.text == payload["text"]
        assert saved.created_at is not None
