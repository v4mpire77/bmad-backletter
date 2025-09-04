import os
from fastapi.testclient import TestClient

os.environ.setdefault("SECRET_KEY", "test")
os.environ.setdefault("AUTH_PEPPER", "pepper")

from blackletter_api.main import app
from blackletter_api.models.schemas import Rulepack, Detector


def test_detect_endpoint(monkeypatch):
    det = Detector(id="d1", anchors_any=["must"], weak_nearby={"any": "@hedges"})
    rp = Rulepack(meta={}, detectors=[det], shared_lexicon={"hedges": ["may"]})
    monkeypatch.setattr(
        "blackletter_api.routers.analysis.load_rulepack", lambda: rp
    )

    client = TestClient(app)
    resp = client.post("/api/analysis/abc/detect", json={"text": "must act"})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and data[0]["verdict"] == "pass"
