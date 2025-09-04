import os
import shutil
import uuid
from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from blackletter_api.services import storage

from blackletter_api.main import app
from blackletter_api.database import Base, get_db
from blackletter_api.models.entities import Analysis

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test database
Base.metadata.create_all(bind=engine)


# --- Dependency Override ---
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def auth_client(tmp_path):
    """Return a TestClient with auth header and isolated DATA_ROOT."""
    data_root = tmp_path / "data"
    storage.DATA_ROOT = data_root
    with TestClient(app) as c:
        c.headers["Authorization"] = "Bearer test-token"
        yield c
    shutil.rmtree(data_root, ignore_errors=True)


# --- Test Cases ---

def test_upload_contract_success(auth_client):
    """
    Tests the successful upload of a valid contract file.
    Verifies that the API responds correctly and that an Analysis record
    is created in the database.
    """
    # Create a dummy file to upload
    sample_content = b"controller instructions"
    dummy_file = ("test_contract.pdf", BytesIO(sample_content), "application/pdf")

    # Make the request to the test client
    response = auth_client.post(
        "/api/contracts",
        files={"file": dummy_file}
    )

    # --- Assertions ---
    # 1. Check the HTTP response
    assert response.status_code == 201
    response_data = response.json()
    assert "job_id" in response_data
    assert "analysis_id" in response_data
    assert response_data["status"] == "queued"
    analysis_id = response_data["analysis_id"]

    # 2. Check the database state
    db = TestingSessionLocal()
    analysis_record = db.query(Analysis).filter(Analysis.id == uuid.UUID(analysis_id)).first()
    db.close()

    assert analysis_record is not None
    assert analysis_record.filename == "test_contract.pdf"
    # The size is updated after saving, so we need to check it from the original content
    assert analysis_record.size_bytes == len(sample_content)
    assert analysis_record.mime_type == "application/pdf"

def teardown_module(module):
    """Clean up the test database file after all tests run."""
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_temp.db"):
        os.remove("./test_temp.db")
