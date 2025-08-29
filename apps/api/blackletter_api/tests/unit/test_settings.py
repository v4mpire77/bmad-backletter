"""
Unit tests for the settings service.
"""
import os
import json
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, mock_open

import pytest

from ...models.schemas import OrgSettings, SettingsUpdateRequest
from ...services.settings import (
    _load_settings_from_file,
    _save_settings_to_file,
    _load_settings_from_env,
    get_org_settings,
    update_org_settings,
    SETTINGS_FILE_PATH
)


class TestSettingsService:
    """Test cases for the settings service."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Ensure we're using a test-specific settings file
        self.test_settings_path = Path(".data") / "test_org_settings.json"
        # Patch the SETTINGS_FILE_PATH to use our test file
        self.settings_patch = patch('blackletter_api.services.settings.SETTINGS_FILE_PATH', self.test_settings_path)
        self.settings_patch.start()

    def teardown_method(self):
        """Tear down test fixtures after each test method."""
        # Stop the patch
        self.settings_patch.stop()
        # Clean up test settings file
        if self.test_settings_path.exists():
            self.test_settings_path.unlink()
        # Clean up the .data directory if it's empty
        data_dir = self.test_settings_path.parent
        try:
            data_dir.rmdir()
        except OSError:
            # Directory not empty, that's fine
            pass

    def test_load_settings_from_file_when_file_does_not_exist(self):
        """Test loading settings when the file doesn't exist."""
        # Ensure the file doesn't exist
        if self.test_settings_path.exists():
            self.test_settings_path.unlink()
        
        settings = _load_settings_from_file()
        assert isinstance(settings, OrgSettings)
        assert settings.llm_provider == "none"
        assert settings.ocr_enabled is False
        assert settings.retention_days == 30

    def test_load_settings_from_file_when_file_exists(self):
        """Test loading settings when the file exists."""
        # Create a test settings file
        test_settings = {
            "llm_provider": "default",
            "ocr_enabled": True,
            "retention_days": 60
        }
        
        self.test_settings_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.test_settings_path, "w") as f:
            json.dump(test_settings, f)
        
        settings = _load_settings_from_file()
        assert isinstance(settings, OrgSettings)
        assert settings.llm_provider == "default"
        assert settings.ocr_enabled is True
        assert settings.retention_days == 60

    def test_save_settings_to_file(self):
        """Test saving settings to file."""
        settings = OrgSettings(
            llm_provider="default",
            ocr_enabled=True,
            retention_days=45
        )
        
        _save_settings_to_file(settings)
        
        # Verify the file was created with correct content
        assert self.test_settings_path.exists()
        with open(self.test_settings_path, "r") as f:
            saved_settings = json.load(f)
        
        assert saved_settings["llm_provider"] == "default"
        assert saved_settings["ocr_enabled"] is True
        assert saved_settings["retention_days"] == 45

    @patch.dict(os.environ, {
        "LLM_PROVIDER": "default",
        "OCR_ENABLED": "true",
        "RETENTION_DAYS": "90"
    })
    def test_load_settings_from_env(self):
        """Test loading settings from environment variables."""
        # First create a file with different settings
        file_settings = OrgSettings(
            llm_provider="none",
            ocr_enabled=False,
            retention_days=30
        )
        _save_settings_to_file(file_settings)
        
        # Load settings (should use env vars)
        settings = _load_settings_from_env()
        
        # Should use environment variables
        assert settings.llm_provider == "default"
        assert settings.ocr_enabled is True
        assert settings.retention_days == 90

    def test_get_org_settings(self):
        """Test getting organization settings."""
        settings = get_org_settings()
        assert isinstance(settings, OrgSettings)

    def test_update_org_settings(self):
        """Test updating organization settings."""
        # Create initial settings
        initial_settings = OrgSettings(
            llm_provider="none",
            ocr_enabled=False,
            retention_days=30
        )
        _save_settings_to_file(initial_settings)
        
        # Update settings
        update_request = SettingsUpdateRequest(
            llm_provider="default",
            ocr_enabled=True
        )
        
        updated_settings = update_org_settings(update_request, updated_by="test_user")
        
        # Verify updates were applied
        assert updated_settings.llm_provider == "default"
        assert updated_settings.ocr_enabled is True
        assert updated_settings.retention_days == 30  # Should remain unchanged
        assert updated_settings.updated_by == "test_user"
        assert updated_settings.updated_at is not None

    def test_update_org_settings_with_no_changes(self):
        """Test updating organization settings with no changes."""
        # Create initial settings
        initial_settings = OrgSettings(
            llm_provider="default",
            ocr_enabled=True,
            retention_days=45
        )
        _save_settings_to_file(initial_settings)
        
        # Update with empty request (no changes)
        update_request = SettingsUpdateRequest()
        
        updated_settings = update_org_settings(update_request, updated_by="test_user")
        
        # Should be the same as initial settings but with updated audit fields
        assert updated_settings.llm_provider == "default"
        assert updated_settings.ocr_enabled is True
        assert updated_settings.retention_days == 45
        assert updated_settings.updated_by == "test_user"
        assert updated_settings.updated_at is not None