"""Test Gemini adapter functionality."""
if __package__ is None or __package__ == "":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from backend.services import llm  # type: ignore
else:
    from ..services import llm

from unittest.mock import Mock, patch


def test_generate_text(monkeypatch):
    """Test generate_text function with mocked Gemini client."""
    monkeypatch.setenv("LLM_PROVIDER", "stub")
    with patch('backend.services.llm.GeminiClient') as mock_client_class:
        # Mock the client instance
        mock_client = Mock()
        mock_client.generate.return_value = "Generated text response"
        mock_client_class.return_value = mock_client
        
        # Call the function
        result = llm.generate_text("test prompt", system="test system")
        
        # Verify the client was created and called correctly
        mock_client_class.assert_called_once()
        mock_client.generate.assert_called_once_with("test prompt", system="test system")
        assert result == "Generated text response"
