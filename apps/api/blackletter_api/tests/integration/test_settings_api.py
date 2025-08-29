"""
Integration tests for the settings API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

from blackletter_api.main import app
from blackletter_api.models.schemas import OrgSettings, SettingsUpdateRequest

client = TestClient(app)


class TestSettingsAPI:
    """Test cases for the settings API endpoints."""

    def test_get_settings(self):
        """Test getting organization settings."""
        response = client.get("/api/admin/settings")
        assert response.status_code == 200
        
        settings = OrgSettings(**response.json())
        assert settings.llm_provider in ["none", "default"]
        assert isinstance(settings.ocr_enabled, bool)
        assert isinstance(settings.retention_days, int)

    def test_update_settings(self):
        """Test updating organization settings."""
        # First get current settings
        response = client.get("/api/admin/settings")
        assert response.status_code == 200
        original_settings = OrgSettings(**response.json())
        
        # Update settings
        update_data = {
            "llm_provider": "default",
            "ocr_enabled": True,
            "retention_days": 90
        }
        
        response = client.put("/api/admin/settings", json=update_data)
        assert response.status_code == 200
        
        updated_settings = OrgSettings(**response.json())
        assert updated_settings.llm_provider == "default"
        assert updated_settings.ocr_enabled is True
        assert updated_settings.retention_days == 90
        assert updated_settings.updated_at is not None
        assert updated_settings.updated_by == "admin"

    def test_partial_update_settings(self):
        """Test partially updating organization settings."""
        # Update only one field
        update_data = {
            "ocr_enabled": False
        }
        
        response = client.put("/api/admin/settings", json=update_data)
        assert response.status_code == 200
        
        updated_settings = OrgSettings(**response.json())
        assert updated_settings.ocr_enabled is False
        # Other fields should remain unchanged
        assert updated_settings.llm_provider in ["none", "default"]

    def test_get_settings_audit_log(self):
        """Test getting settings audit log."""
        response = client.get("/api/admin/settings/audit")
        assert response.status_code == 200
        assert isinstance(response.json(), list)