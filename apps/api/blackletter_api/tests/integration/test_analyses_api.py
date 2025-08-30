import pytest
from fastapi.testclient import TestClient
from ...main import app
from ...orchestrator.state import orchestrator

client = TestClient(app)


def test_list_analyses():
    """Test listing analyses."""
    # Clear the orchestrator store
    orchestrator._store.clear()
    
    # Add a test analysis
    analysis_id = orchestrator.intake("test_contract.pdf")
    
    response = client.get("/api/analyses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == analysis_id
    assert data[0]["filename"] == "test_contract.pdf"


def test_get_analysis_summary():
    """Test getting a specific analysis summary."""
    # Clear the orchestrator store
    orchestrator._store.clear()
    
    # Add a test analysis
    analysis_id = orchestrator.intake("test_contract.pdf")
    
    response = client.get(f"/api/analyses/{analysis_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == analysis_id
    assert data["filename"] == "test_contract.pdf"


def test_get_analysis_summary_not_found():
    """Test getting a non-existent analysis summary."""
    response = client.get("/api/analyses/non-existent-id")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Analysis not found"


def test_get_analysis_findings():
    """Test getting findings for a specific analysis."""
    # Clear the orchestrator store
    orchestrator._store.clear()
    
    # Add a test analysis
    analysis_id = orchestrator.intake("test_contract.pdf")
    
    # Add a test finding
    test_finding = {
        "detector_id": "test_detector",
        "rule_id": "test_rule",
        "verdict": "pass",
        "snippet": "This is a test snippet.",
        "page": 1,
        "start": 0,
        "end": 25,
        "rationale": "This is a test rationale."
    }
    orchestrator.advance(analysis_id, orchestrator._store[analysis_id].state, test_finding)
    
    response = client.get(f"/api/analyses/{analysis_id}/findings")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["detector_id"] == "test_detector"
    assert data[0]["snippet"] == "This is a test snippet."


def test_get_analysis_findings_not_found():
    """Test getting findings for a non-existent analysis."""
    response = client.get("/api/analyses/non-existent-id/findings")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Analysis not found"