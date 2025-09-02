import json
import uuid
from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from blackletter_api.main import app
from blackletter_api.database import Base, get_db
from blackletter_api.models.entities import ExtractionArtifact, EvidenceArtifact
from blackletter_api.services import tasks
from blackletter_api.services import artifacts as artifact_service
from blackletter_api.services.storage import analysis_dir


# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# --- Dependency Override ---
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# --- Patches for services ---
class DummyRedis:
    def __init__(self):
        self.store = {}

    def hset(self, key, mapping):
        self.store[key] = mapping

    def hgetall(self, key):
        return self.store.get(key, {})

    def exists(self, key):
        return key in self.store


def fake_run_extraction(analysis_id, source_path, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    text = source_path.read_text(encoding="utf-8")
    payload = {
        "text_path": "extracted.txt",
        "page_map": [{"page": 1, "start": 0, "end": len(text)}],
        "sentences": [{"page": 1, "start": 0, "end": len(text), "text": text}],
        "meta": {},
    }
    (out_dir / "extracted.txt").write_text(text, encoding="utf-8")
    (out_dir / "extraction.json").write_text(json.dumps(payload), encoding="utf-8")
    (out_dir / "sentences.json").write_text(
        json.dumps({"sentences": payload["sentences"], "page_map": payload["page_map"]}),
        encoding="utf-8",
    )
    return out_dir / "extraction.json"


def fake_run_detectors(analysis_id, extraction_json_path):
    with open(extraction_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    s = data["sentences"][0]
    finding = {
        "detector_id": "demo",
        "rule_id": "demo",
        "verdict": "pass",
        "snippet": s["text"],
        "page": s["page"],
        "start": s["start"],
        "end": s["end"],
        "rationale": "demo",
    }
    findings_path = analysis_dir(analysis_id) / "findings.json"
    findings_path.write_text(json.dumps([finding]), encoding="utf-8")
    from blackletter_api.models.schemas import Finding

    return [Finding(**finding)]


# Apply patches
artifact_service.SessionLocal = TestingSessionLocal
tasks.redis_client = DummyRedis()
tasks.run_extraction = fake_run_extraction
tasks.run_detectors = fake_run_detectors


def run_sync(*args, **kwargs):
    return tasks.process_job(*args, **kwargs)


tasks.process_job.delay = run_sync


# --- Test Case ---
def test_contract_processing_flow(tmp_path):
    content = "controller instructions"
    dummy_file = ("test.pdf", BytesIO(content.encode("utf-8")), "application/pdf")
    response = client.post("/v1/contracts", files={"file": dummy_file})
    assert response.status_code == 201
    data = response.json()
    analysis_id = data["analysis_id"]

    db = TestingSessionLocal()
    art = (
        db.query(ExtractionArtifact)
        .filter(ExtractionArtifact.analysis_id == uuid.UUID(analysis_id))
        .first()
    )
    evid = (
        db.query(EvidenceArtifact)
        .filter(EvidenceArtifact.analysis_id == uuid.UUID(analysis_id))
        .first()
    )
    db.close()
    assert art is not None
    assert evid is not None

    resp_findings = client.get(f"/v1/docs/{analysis_id}/findings")
    assert resp_findings.status_code == 200
    assert resp_findings.json()[0]["snippet"] == content

    resp_html = client.get(f"/v1/exports/{analysis_id}.html")
    assert resp_html.status_code == 200
    assert content in resp_html.text


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)
    Path("./test_temp.db").unlink(missing_ok=True)
    import shutil

    shutil.rmtree(".data", ignore_errors=True)
