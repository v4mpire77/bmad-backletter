"""Tests for Story 2.4 - Token Ledger & Caps"""
import pytest
import uuid
from unittest.mock import patch, MagicMock

from blackletter_api.services.llm_gate import LLMGate, get_llm_gate, simulate_llm_call
from blackletter_api.services.metrics import MetricsService, get_metrics_service
from blackletter_api.models.entities import Metric
from blackletter_api.core_config_loader import CoreConfig, BudgetConfig


def test_llm_gate_initialization():
    """Test LLM gate initializes with config."""
    gate = LLMGate()
    
    assert gate.hard_cap >= 0
    assert gate.on_exceed in ["needs_review", "stop", "ignore"]


def test_llm_gate_check_token_allowance_within_limit():
    """Test token allowance check when within limit."""
    gate = LLMGate()
    gate.hard_cap = 1000
    
    analysis_id = str(uuid.uuid4())
    
    # Mock current usage to be low
    with patch.object(gate, 'get_current_token_usage', return_value=100):
        allowed, reason = gate.check_token_allowance(analysis_id, 200)
        
        assert allowed is True
        assert reason is None


def test_llm_gate_check_token_allowance_exceeds_limit():
    """Test token allowance check when exceeding limit."""
    gate = LLMGate()
    gate.hard_cap = 1000
    
    analysis_id = str(uuid.uuid4())
    
    # Mock current usage to be high
    with patch.object(gate, 'get_current_token_usage', return_value=900):
        allowed, reason = gate.check_token_allowance(analysis_id, 200)
        
        assert allowed is False
        assert "token_cap" in reason
        assert "1100" in reason  # projected total
        assert "1000" in reason  # limit


def test_llm_gate_record_token_usage():
    """Test recording token usage creates metrics."""
    gate = LLMGate()
    analysis_id = str(uuid.uuid4())
    
    # Mock database session
    mock_session = MagicMock()
    mock_session.query().filter().first.return_value = None  # No existing metric
    
    with patch('blackletter_api.services.llm_gate.SessionLocal', return_value=mock_session):
        gate.record_token_usage(analysis_id, 150, True)
        
        # Verify metric was added
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()


def test_llm_gate_enforce_cap_on_findings():
    """Test that cap enforcement marks incomplete findings as needs_review."""
    gate = LLMGate()
    gate.hard_cap = 1000
    
    analysis_id = str(uuid.uuid4())
    
    findings = [
        {"id": "1", "status": "completed", "rule": "A28_3_a"},
        {"id": "2", "status": "pending", "rule": "A28_3_b"},
        {"id": "3", "status": "incomplete", "rule": "A28_3_c"},
        {"id": "4", "status": None, "rule": "A28_3_d"},
    ]
    
    # Mock high usage to trigger cap
    with patch.object(gate, 'get_current_token_usage', return_value=1500):
        modified_findings = gate.enforce_cap_on_findings(analysis_id, findings)
        
        # Check that incomplete findings are marked as needs_review
        completed_finding = next(f for f in modified_findings if f["id"] == "1")
        assert completed_finding["status"] == "completed"  # Should not change
        
        pending_finding = next(f for f in modified_findings if f["id"] == "2")
        assert pending_finding["status"] == "needs_review"
        assert pending_finding["reason"] == "token_cap"
        
        incomplete_finding = next(f for f in modified_findings if f["id"] == "3")
        assert incomplete_finding["status"] == "needs_review"
        
        none_status_finding = next(f for f in modified_findings if f["id"] == "4")
        assert none_status_finding["status"] == "needs_review"


def test_simulate_llm_call_within_cap():
    """Test simulated LLM call when within token cap."""
    analysis_id = str(uuid.uuid4())
    snippet = "This is a test snippet for LLM processing."
    
    with patch('blackletter_api.services.llm_gate.get_llm_gate') as mock_get_gate:
        mock_gate = MagicMock()
        mock_gate.check_token_allowance.return_value = (True, None)
        mock_get_gate.return_value = mock_gate
        
        success, response, tokens_used = simulate_llm_call(analysis_id, snippet)
        
        assert success is True
        assert "LLM response" in response
        assert tokens_used > 0
        
        # Verify gate was called correctly
        mock_gate.check_token_allowance.assert_called_once()
        mock_gate.record_token_usage.assert_called_once()


def test_simulate_llm_call_exceeds_cap():
    """Test simulated LLM call when exceeding token cap."""
    analysis_id = str(uuid.uuid4())
    snippet = "This is a test snippet for LLM processing."
    
    with patch('blackletter_api.services.llm_gate.get_llm_gate') as mock_get_gate:
        mock_gate = MagicMock()
        mock_gate.check_token_allowance.return_value = (False, "token_cap: exceeded limit")
        mock_get_gate.return_value = mock_gate
        
        success, response, tokens_used = simulate_llm_call(analysis_id, snippet)
        
        assert success is False
        assert "Token cap exceeded" in response
        assert tokens_used == 0
        
        # Verify error was recorded
        mock_gate.record_token_usage.assert_called_once_with(analysis_id, 0, False, "token_cap: exceeded limit")


def test_metrics_service_get_admin_metrics():
    """Test metrics service returns admin metrics."""
    service = MetricsService()
    
    # Mock database session with sample metrics
    mock_session = MagicMock()
    mock_metrics = [
        MagicMock(tokens_per_doc=100, llm_invoked=True, processing_time_ms=1200.5, error_reason=None),
        MagicMock(tokens_per_doc=150, llm_invoked=False, processing_time_ms=800.0, error_reason=None),
        MagicMock(tokens_per_doc=0, llm_invoked=False, processing_time_ms=500.0, error_reason="token_cap"),
    ]
    mock_session.query().order_by().limit().all.return_value = mock_metrics
    
    with patch('blackletter_api.services.metrics.SessionLocal', return_value=mock_session):
        metrics = service.get_admin_metrics()
        
        assert "avg_tokens_per_doc" in metrics
        assert "llm_usage_percent" in metrics
        assert "p95_latency_ms" in metrics
        assert "explainability_rate" in metrics
        assert "total_analyses" in metrics
        assert "cap_exceeded_count" in metrics
        
        assert metrics["total_analyses"] == 3
        assert metrics["cap_exceeded_count"] == 1


def test_metrics_service_record_analysis_completion():
    """Test recording analysis completion metrics."""
    service = MetricsService()
    analysis_id = str(uuid.uuid4())
    
    # Mock database session
    mock_session = MagicMock()
    mock_session.query().filter().first.return_value = None  # No existing metric
    
    with patch('blackletter_api.services.metrics.SessionLocal', return_value=mock_session):
        service.record_analysis_completion(
            analysis_id=analysis_id,
            processing_time_ms=1500.0,
            detection_count=8,
            tokens_used=250,
            llm_invoked=True
        )
        
        # Verify metric was added
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()


def test_token_cap_integration():
    """Integration test for token cap functionality."""
    gate = LLMGate()
    gate.hard_cap = 500  # Low cap for testing
    
    analysis_id = str(uuid.uuid4())
    
    # Mock zero initial usage
    with patch.object(gate, 'get_current_token_usage', return_value=0):
        # First call should succeed
        allowed, reason = gate.check_token_allowance(analysis_id, 300)
        assert allowed is True
        
    # Mock high usage after first call
    with patch.object(gate, 'get_current_token_usage', return_value=400):
        # Second call should fail
        allowed, reason = gate.check_token_allowance(analysis_id, 200)
        assert allowed is False
        assert "token_cap" in reason


def test_llm_gate_handles_zero_tokens():
    """Test LLM gate handles zero token usage correctly."""
    gate = LLMGate()
    analysis_id = str(uuid.uuid4())
    
    # Mock database session
    mock_session = MagicMock()
    mock_session.query().filter().first.return_value = None
    
    with patch('blackletter_api.services.llm_gate.SessionLocal', return_value=mock_session):
        gate.record_token_usage(analysis_id, 0, False)
        
        # Should still record the metric
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()