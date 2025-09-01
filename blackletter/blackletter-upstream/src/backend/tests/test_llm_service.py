"""
Test module for the LLMService wrapper class.
"""

import asyncio
import sys
import os
from unittest.mock import AsyncMock, patch

# Add the parent directory to the path so we can import llm_service
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_service import LLMService


def test_llm_service_initialization(monkeypatch):
    """Test that LLMService initializes correctly."""
    monkeypatch.setenv("LLM_PROVIDER", "stub")
    service = LLMService()
    assert hasattr(service, 'adapter')
    assert hasattr(service, 'provider')
    assert hasattr(service, 'analyze_contract')
    assert hasattr(service, 'get_provider_info')


def test_get_provider_info(monkeypatch):
    """Test provider information retrieval."""
    monkeypatch.setenv("LLM_PROVIDER", "stub")
    service = LLMService()
    info = service.get_provider_info()
    
    required_keys = ["provider", "model", "gemini_configured", 
                    "ollama_available", "init_error"]
    
    for key in required_keys:
        assert key in info
    
    assert isinstance(info["gemini_configured"], bool)
    assert isinstance(info["ollama_available"], bool)


def test_analyze_contract(monkeypatch):
    """Test contract analysis functionality."""
    monkeypatch.setenv("LLM_PROVIDER", "stub")
    service = LLMService()

    # Mock the adapter's analyze_contract method
    mock_result = {
        "summary": "Test summary",
        "risks": ["Test risk"],
        "dates": [],
        "error": None,
    }

    async def fake_analyze(text: str):
        return mock_result

    with patch.object(service.adapter, "analyze_contract", AsyncMock(side_effect=fake_analyze)) as mock_analyze:
        result = asyncio.run(service.analyze_contract("Test contract text"))

        assert result == mock_result
        mock_analyze.assert_awaited_once_with("Test contract text")


if __name__ == "__main__":
    # Run a simple test
    service = LLMService()
    print(f"✅ LLMService created successfully")
    print(f"Provider: {service.provider}")
    
    info = service.get_provider_info()
    print(f"Provider info keys: {list(info.keys())}")
