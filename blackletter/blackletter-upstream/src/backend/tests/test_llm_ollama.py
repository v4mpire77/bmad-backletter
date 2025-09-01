"""
NOTE: These tests are skipped because Ollama functionality has been removed
from services/llm.py in favor of a Gemini-only implementation.
Ollama support is still available through the LLMAdapter in backend/app/core/llm_adapter.py.
"""

if __package__ is None or __package__ == "":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from backend.services import llm  # type: ignore
else:
    from ..services import llm

import pytest
from unittest.mock import Mock, patch


class DummyOllamaClient:
    def generate(self, prompt, system=None, max_tokens=800):
        return "Ollama response"


@pytest.mark.skip(reason="Ollama functionality removed from services/llm.py - use LLMAdapter instead")
def test_ollama_generate_text(monkeypatch):
    """Test Ollama provider through generate_text function"""
    monkeypatch.setenv("PROVIDER_ORDER", "ollama")
    monkeypatch.setattr(llm, "_client_for", lambda provider, models: DummyOllamaClient())
    result = llm.generate_text("hello")
    assert result == "Ollama response"


@pytest.mark.skip(reason="Ollama functionality removed from services/llm.py - use LLMAdapter instead")
def test_ollama_client_basic():
    """Test OllamaClient basic functionality with mocked requests"""
    with patch('requests.post') as mock_post:
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"response": "Test Ollama response"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        client = llm.OllamaClient("llama3.1")
        result = client.generate("Hello world")
        
        assert result == "Test Ollama response"
        mock_post.assert_called_once()
        
        # Verify the request was made correctly
        call_args = mock_post.call_args
        assert call_args[1]['json']['model'] == 'llama3.1'
        assert call_args[1]['json']['prompt'] == 'Hello world'
        assert call_args[1]['json']['stream'] is False


@pytest.mark.skip(reason="Ollama functionality removed from services/llm.py - use LLMAdapter instead")
def test_ollama_client_with_system():
    """Test OllamaClient with system message"""
    with patch('requests.post') as mock_post:
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {"response": "System response"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        client = llm.OllamaClient("llama3.1")
        result = client.generate("Hello", system="You are a helpful assistant")
        
        assert result == "System response"
        
        # Verify system message was included in prompt
        call_args = mock_post.call_args
        expected_prompt = "System: You are a helpful assistant\n\nHello"
        assert call_args[1]['json']['prompt'] == expected_prompt


@pytest.mark.skip(reason="Ollama functionality removed from services/llm.py - use LLMAdapter instead")
def test_ollama_client_error_handling():
    """Test OllamaClient error handling"""
    with patch('requests.post') as mock_post:
        # Mock request exception
        mock_post.side_effect = Exception("Connection error")
        
        client = llm.OllamaClient("llama3.1")
        
        with pytest.raises(RuntimeError) as exc_info:
            client.generate("Hello")
        
        assert "Ollama error: Connection error" in str(exc_info.value)


@pytest.mark.skip(reason="Ollama functionality removed from services/llm.py - use LLMAdapter instead")
def test_ollama_model_prefs():
    """Test that Ollama model can be configured via environment"""
    import os
    original_model = os.environ.get("OLLAMA_MODEL")
    
    try:
        os.environ["OLLAMA_MODEL"] = "custom-model"
        # Need to reimport or recreate ModelPrefs to pick up new env var
        import importlib
        importlib.reload(llm)
        models = llm.ModelPrefs()
        assert models.ollama == "custom-model"
    finally:
        if original_model is not None:
            os.environ["OLLAMA_MODEL"] = original_model
        elif "OLLAMA_MODEL" in os.environ:
            del os.environ["OLLAMA_MODEL"]
        # Reload again to restore original state
        import importlib
        importlib.reload(llm)


@pytest.mark.skip(reason="Ollama functionality removed from services/llm.py - use LLMAdapter instead")
def test_provider_order_includes_ollama():
    """Test that ollama is included in default provider order"""
    import os
    original_order = os.environ.get("PROVIDER_ORDER")
    
    try:
        # Test default order includes ollama
        if "PROVIDER_ORDER" in os.environ:
            del os.environ["PROVIDER_ORDER"]
        
        order = llm._provider_order()
        assert "ollama" in order
        
        # Test custom order with ollama first
        os.environ["PROVIDER_ORDER"] = "ollama,gemini"
        order = llm._provider_order()
        assert order == ["ollama", "gemini"]
        
    finally:
        if original_order is not None:
            os.environ["PROVIDER_ORDER"] = original_order
        elif "PROVIDER_ORDER" in os.environ:
            del os.environ["PROVIDER_ORDER"]