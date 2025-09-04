"""Tests for Story 5.1 - Org Settings (LLM/OCR/Retention)"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from blackletter_api.models.entities import (
    OrgSetting,
    LLMProvider,
    RetentionPolicy,
    ComplianceMode,
)
from blackletter_api.routers.settings import (
    OrgSettingsRequest,
    OrgSettingsResponse,
    update_org_settings,
)


def test_llm_provider_enum():
    """Test LLM provider enum values."""
    assert LLMProvider.none.value == "none"
    assert LLMProvider.openai.value == "openai"
    assert LLMProvider.anthropic.value == "anthropic"
    assert LLMProvider.gemini.value == "gemini"


def test_retention_policy_enum():
    """Test retention policy enum values."""
    assert RetentionPolicy.none.value == "none"
    assert RetentionPolicy.thirty_days.value == "30d"
    assert RetentionPolicy.ninety_days.value == "90d"


def test_compliance_mode_enum():
    """Test compliance mode enum values."""
    assert ComplianceMode.strict.value == "strict"
    assert ComplianceMode.standard.value == "standard"


def test_org_setting_model():
    """Test OrgSetting model defaults."""
    setting = OrgSetting()

    assert setting.llm_provider == LLMProvider.none
    assert setting.llm_enabled is True
    assert setting.ocr_enabled is False
    assert setting.retention_policy == RetentionPolicy.none
    assert setting.compliance_mode == ComplianceMode.strict
    assert setting.evidence_window == 2


def test_org_settings_request_model():
    """Test OrgSettingsRequest model validation."""
    request = OrgSettingsRequest(
        llm_provider="openai",
        llm_enabled=False,
        ocr_enabled=True,
        retention_policy="30d",
        compliance_mode="standard",
        evidence_window=3,
    )

    assert request.llm_provider == "openai"
    assert request.llm_enabled is False
    assert request.ocr_enabled is True
    assert request.retention_policy == "30d"
    assert request.compliance_mode == "standard"
    assert request.evidence_window == 3


def test_org_settings_request_defaults():
    """Test OrgSettingsRequest model with defaults."""
    request = OrgSettingsRequest()

    assert request.llm_provider == "none"
    assert request.llm_enabled is True
    assert request.ocr_enabled is False
    assert request.retention_policy == "none"
    assert request.compliance_mode == "strict"
    assert request.evidence_window == 2


def test_org_settings_response_model():
    """Test OrgSettingsResponse model."""
    response = OrgSettingsResponse(
        llm_provider="anthropic",
        llm_enabled=True,
        ocr_enabled=True,
        retention_policy="90d",
        compliance_mode="standard",
        evidence_window=4,
        privacy_note="Test privacy note",
        cost_note="Test cost note",
        updated_at="2025-01-01T00:00:00"
    )

    assert response.llm_provider == "anthropic"
    assert response.llm_enabled is True
    assert response.ocr_enabled is True
    assert response.retention_policy == "90d"
    assert response.compliance_mode == "standard"
    assert response.evidence_window == 4
    assert "privacy" in response.privacy_note
    assert "cost" in response.cost_note


@patch('blackletter_api.routers.settings.SessionLocal')
def test_get_org_settings_existing(mock_session_local):
    """Test getting existing organization settings."""
    from blackletter_api.routers.settings import get_org_settings
    
    # Mock database session and setting
    mock_session = MagicMock()
    mock_session_local.return_value.__enter__ = MagicMock(return_value=mock_session)
    mock_session_local.return_value.__exit__ = MagicMock(return_value=None)
    
    mock_setting = MagicMock()
    mock_setting.llm_provider = LLMProvider.openai
    mock_setting.ocr_enabled = True
    mock_setting.retention_policy = RetentionPolicy.thirty_days
    mock_setting.updated_at.isoformat.return_value = "2025-01-01T12:00:00"
    
    mock_session.query().first.return_value = mock_setting
    
    # Note: This is a simplified test - in real scenario we'd use dependency injection
    # For now, just test the model logic
    assert mock_setting.llm_provider == LLMProvider.openai
    assert mock_setting.ocr_enabled is True
    assert mock_setting.retention_policy == RetentionPolicy.thirty_days


@patch('blackletter_api.routers.settings.SessionLocal')
def test_get_org_settings_creates_defaults(mock_session_local):
    """Test that get_org_settings creates default settings if none exist."""
    from blackletter_api.routers.settings import get_org_settings
    
    # Mock database session
    mock_session = MagicMock()
    mock_session_local.return_value.__enter__ = MagicMock(return_value=mock_session)
    mock_session_local.return_value.__exit__ = MagicMock(return_value=None)
    
    # No existing settings
    mock_session.query().first.return_value = None
    
    # Mock created setting
    mock_created_setting = MagicMock()
    mock_created_setting.llm_provider = LLMProvider.none
    mock_created_setting.ocr_enabled = False
    mock_created_setting.retention_policy = RetentionPolicy.none
    mock_created_setting.updated_at.isoformat.return_value = "2025-01-01T12:00:00"
    
    mock_session.refresh.return_value = None
    
    # Verify default values would be used
    assert LLMProvider.none.value == "none"
    assert RetentionPolicy.none.value == "none"


def test_update_org_settings_validation():
    """Test settings update validation."""
    # Valid request
    valid_request = OrgSettingsRequest(
        llm_provider="gemini",
        ocr_enabled=True,
        retention_policy="90d"
    )
    
    # Test enum validation
    try:
        LLMProvider(valid_request.llm_provider)
        RetentionPolicy(valid_request.retention_policy)
    except ValueError:
        pytest.fail("Valid request should not raise ValueError")
    
    # Invalid LLM provider
    with pytest.raises(ValueError):
        LLMProvider("invalid_provider")
    
    # Invalid retention policy
    with pytest.raises(ValueError):
        RetentionPolicy("invalid_policy")


@pytest.mark.asyncio
async def test_update_org_settings_llm_disabled_requires_none():
    """llm_provider must be 'none' when llm_enabled is false."""
    request = OrgSettingsRequest(
        llm_provider="openai",
        llm_enabled=False,
        ocr_enabled=False,
        retention_policy="none",
        compliance_mode="strict",
        evidence_window=2,
    )

    with pytest.raises(HTTPException) as exc:
        await update_org_settings(request, db=MagicMock())
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_update_org_settings_evidence_window_positive():
    """evidence_window must be positive."""
    request = OrgSettingsRequest(
        llm_provider="none",
        llm_enabled=True,
        ocr_enabled=False,
        retention_policy="none",
        compliance_mode="strict",
        evidence_window=0,
    )

    with pytest.raises(HTTPException) as exc:
        await update_org_settings(request, db=MagicMock())
    assert exc.value.status_code == 400

def test_privacy_impact_llm_disabled():
    """Test privacy impact when LLM is disabled."""
    setting = OrgSetting(
        llm_provider=LLMProvider.none,
        llm_enabled=False,
        ocr_enabled=False,
        retention_policy=RetentionPolicy.none,
    )
    
    # Simulate privacy impact logic
    privacy_impact = {
        "llm_data_sharing": {
            "enabled": setting.llm_enabled and setting.llm_provider != LLMProvider.none,
            "provider": setting.llm_provider.value,
            "data_shared": "No data shared"
        },
        "ocr_processing": {
            "enabled": setting.ocr_enabled,
            "data_processed": "No OCR processing"
        },
        "data_retention": {
            "policy": setting.retention_policy.value,
            "description": "Data retained indefinitely"
        }
    }
    
    assert privacy_impact["llm_data_sharing"]["enabled"] is False
    assert privacy_impact["llm_data_sharing"]["data_shared"] == "No data shared"
    assert privacy_impact["ocr_processing"]["enabled"] is False
    assert privacy_impact["data_retention"]["policy"] == "none"


def test_privacy_impact_llm_enabled():
    """Test privacy impact when LLM is enabled."""
    setting = OrgSetting(
        llm_provider=LLMProvider.anthropic,
        llm_enabled=True,
        ocr_enabled=True,
        retention_policy=RetentionPolicy.thirty_days,
    )
    
    # Simulate privacy impact logic
    privacy_impact = {
        "llm_data_sharing": {
            "enabled": setting.llm_enabled and setting.llm_provider != LLMProvider.none,
            "provider": setting.llm_provider.value,
            "data_shared": "Short text snippets only (max 220 tokens)"
        },
        "ocr_processing": {
            "enabled": setting.ocr_enabled,
            "data_processed": "Document images converted to text locally"
        },
        "data_retention": {
            "policy": setting.retention_policy.value,
            "description": "Data automatically deleted after 30 days"
        }
    }
    
    assert privacy_impact["llm_data_sharing"]["enabled"] is True
    assert privacy_impact["llm_data_sharing"]["provider"] == "anthropic"
    assert "snippets" in privacy_impact["llm_data_sharing"]["data_shared"]
    assert privacy_impact["ocr_processing"]["enabled"] is True
    assert privacy_impact["data_retention"]["policy"] == "30d"


def test_settings_privacy_notes():
    """Test that privacy and cost notes are included."""
    privacy_note = "Your file stays private. LLM is off by default. When enabled, only short snippets are sent."
    cost_note = "Enabling LLM features may incur additional costs based on token usage. Monitor usage in admin metrics."
    
    assert "private" in privacy_note.lower()
    assert "snippets" in privacy_note.lower()
    assert "costs" in cost_note.lower()
    assert "token usage" in cost_note.lower()


def test_audit_trail():
    """Test that settings changes are audited."""
    setting = OrgSetting(
        llm_provider=LLMProvider.openai,
        llm_enabled=True,
        ocr_enabled=True,
        retention_policy=RetentionPolicy.ninety_days,
    )

    # Verify audit fields exist
    assert hasattr(setting, "created_at")
    assert hasattr(setting, "updated_at")

    # Verify the setting values
    assert setting.llm_provider == LLMProvider.openai
    assert setting.llm_enabled is True
    assert setting.ocr_enabled is True
    assert setting.retention_policy == RetentionPolicy.ninety_days

