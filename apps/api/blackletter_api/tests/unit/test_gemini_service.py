"""
Unit tests for Gemini AI service
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from ...services.gemini_service import GeminiService, GeminiAnalysisResult, GeminiChatResponse


class TestGeminiService:
    """Test cases for Gemini service"""

    def test_service_initialization_without_api_key(self):
        """Test service initialization when API key is not configured"""
        with patch('blackletter_api.services.gemini_service.settings') as mock_settings:
            mock_settings.gemini_api_key = None
            service = GeminiService()

            assert not service.is_available()
            assert service.model is None

    def test_service_initialization_with_api_key(self):
        """Test service initialization when API key is configured"""
        with patch('blackletter_api.services.gemini_service.settings') as mock_settings:
            mock_settings.gemini_api_key = "test_key"
            mock_settings.gemini_model = "gemini-1.5-flash"
            mock_settings.gemini_max_tokens = 2048
            mock_settings.gemini_temperature = 0.7

            with patch('blackletter_api.services.gemini_service.genai') as mock_genai:
                service = GeminiService()

                assert service.is_available()
                assert service.api_key == "test_key"
                mock_genai.configure.assert_called_once_with(api_key="test_key")

    def test_analyze_contract_unavailable_service(self):
        """Test contract analysis when service is not available"""
        service = GeminiService()
        service.model = None  # Simulate unavailable service

        result = service.analyze_contract("test contract")
        assert result is None

    @patch('blackletter_api.services.gemini_service.genai')
    def test_analyze_contract_success(self, mock_genai):
        """Test successful contract analysis"""
        # Setup mocks
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = '{"summary": "Test summary", "key_terms": ["term1"], "risk_factors": ["risk1"], "recommendations": ["rec1"]}'
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        with patch('blackletter_api.services.gemini_service.settings') as mock_settings:
            mock_settings.gemini_api_key = "test_key"
            mock_settings.gemini_model = "gemini-1.5-flash"
            mock_settings.gemini_max_tokens = 2048
            mock_settings.gemini_temperature = 0.7

            service = GeminiService()
            result = service.analyze_contract("test contract", "general")

            assert result is not None
            assert isinstance(result, GeminiAnalysisResult)
            assert result.summary == "Test summary"
            assert result.key_terms == ["term1"]

    @patch('blackletter_api.services.gemini_service.genai')
    def test_summarize_contract_success(self, mock_genai):
        """Test successful contract summarization"""
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = "This is a test summary of the contract."
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        with patch('blackletter_api.services.gemini_service.settings') as mock_settings:
            mock_settings.gemini_api_key = "test_key"
            mock_settings.gemini_model = "gemini-1.5-flash"

            service = GeminiService()
            summary = service.summarize_contract("long contract text")

            assert summary == "This is a test summary of the contract."

    def test_parse_analysis_response_json(self):
        """Test parsing JSON response from Gemini"""
        service = GeminiService()
        mock_response = Mock()
        mock_response.text = '{"summary": "test", "key_terms": ["a", "b"], "risk_factors": ["x"], "recommendations": ["y"]}'

        result = service._parse_analysis_response(mock_response, "test contract")

        assert isinstance(result, GeminiAnalysisResult)
        assert result.summary == "test"
        assert result.key_terms == ["a", "b"]
        assert result.risk_factors == ["x"]
        assert result.recommendations == ["y"]

    def test_parse_analysis_response_plain_text(self):
        """Test parsing plain text response from Gemini"""
        service = GeminiService()
        mock_response = Mock()
        mock_response.text = "This contract has some risks. You should consider reviewing it."

        result = service._parse_analysis_response(mock_response, "test contract")

        assert isinstance(result, GeminiAnalysisResult)
        assert "risks" in result.summary.lower()
        assert len(result.risk_factors) > 0

    def test_chat_response_parsing(self):
        """Test parsing chat response"""
        service = GeminiService()
        mock_response = Mock()
        mock_response.text = '{"answer": "test response", "additional_considerations": ["consideration1"], "follow_up_questions": ["question1"]}'

        result = service._parse_chat_response(mock_response)

        assert isinstance(result, GeminiChatResponse)
        assert result.response == "test response"
        assert result.suggestions == ["consideration1"]
        assert result.follow_up_questions == ["question1"]


class TestGeminiAnalysisResult:
    """Test cases for GeminiAnalysisResult dataclass"""

    def test_dataclass_creation(self):
        """Test creating GeminiAnalysisResult instance"""
        result = GeminiAnalysisResult(
            summary="Test summary",
            key_terms=["term1", "term2"],
            risk_factors=["risk1"],
            recommendations=["rec1", "rec2"],
            confidence_score=0.85,
            raw_response={"test": "data"}
        )

        assert result.summary == "Test summary"
        assert result.key_terms == ["term1", "term2"]
        assert result.confidence_score == 0.85


class TestGeminiChatResponse:
    """Test cases for GeminiChatResponse dataclass"""

    def test_dataclass_creation(self):
        """Test creating GeminiChatResponse instance"""
        response = GeminiChatResponse(
            response="Test response",
            suggestions=["suggestion1"],
            follow_up_questions=["question1", "question2"]
        )

        assert response.response == "Test response"
        assert response.suggestions == ["suggestion1"]
        assert len(response.follow_up_questions) == 2
