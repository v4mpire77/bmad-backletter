"""
Service for managing organization-level settings.
"""
import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

from ..models.schemas import OrgSettings, SettingsUpdateRequest

logger = logging.getLogger(__name__)

# Path to store settings (in production, this should be a secure location)
SETTINGS_FILE_PATH = Path(".data") / "org_settings.json"

# Default settings
DEFAULT_SETTINGS = OrgSettings()


def _ensure_settings_directory():
    """Ensure the settings directory exists."""
    SETTINGS_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)


def _serialize_settings(settings: OrgSettings) -> Dict[str, Any]:
    """Serialize settings to a JSON-serializable dictionary."""
    # Convert to dict and handle datetime serialization
    settings_dict = settings.model_dump()
    if settings_dict.get('updated_at'):
        settings_dict['updated_at'] = settings_dict['updated_at'].isoformat()
    return settings_dict


def _deserialize_settings(data: Dict[str, Any]) -> OrgSettings:
    """Deserialize settings from a dictionary."""
    # Handle datetime deserialization
    if data.get('updated_at'):
        try:
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        except ValueError:
            # If parsing fails, remove the field
            del data['updated_at']
    return OrgSettings(**data)


def _load_settings_from_file() -> OrgSettings:
    """Load settings from file storage."""
    _ensure_settings_directory()
    
    if not SETTINGS_FILE_PATH.exists():
        # Return default settings if file doesn't exist
        return DEFAULT_SETTINGS
    
    try:
        with open(SETTINGS_FILE_PATH, "r") as f:
            data = json.load(f)
            return _deserialize_settings(data)
    except Exception as e:
        logger.warning(f"Failed to load settings from file: {e}. Using defaults.")
        return DEFAULT_SETTINGS


def _save_settings_to_file(settings: OrgSettings):
    """Save settings to file storage."""
    _ensure_settings_directory()
    
    try:
        # Convert to dict and save to file
        settings_dict = _serialize_settings(settings)
        with open(SETTINGS_FILE_PATH, "w") as f:
            json.dump(settings_dict, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save settings to file: {e}")
        raise


def _load_settings_from_env() -> OrgSettings:
    """Load settings from environment variables (overrides file settings)."""
    settings = _load_settings_from_file()
    
    # Override with environment variables if present
    llm_provider = os.getenv("LLM_PROVIDER")
    if llm_provider in ["none", "default"]:
        settings.llm_provider = llm_provider
    
    ocr_enabled = os.getenv("OCR_ENABLED")
    if ocr_enabled is not None:
        settings.ocr_enabled = ocr_enabled.lower() in ["1", "true", "yes"]
    
    retention_days = os.getenv("RETENTION_DAYS")
    if retention_days is not None:
        try:
            settings.retention_days = int(retention_days)
        except ValueError:
            logger.warning(f"Invalid RETENTION_DAYS value: {retention_days}")
    
    return settings


def get_org_settings() -> OrgSettings:
    """
    Get organization settings from environment variables or file storage.
    
    Environment variables take precedence over file storage.
    """
    return _load_settings_from_env()


def update_org_settings(update_request: SettingsUpdateRequest, updated_by: Optional[str] = None) -> OrgSettings:
    """
    Update organization settings and persist them.
    
    Args:
        update_request: The settings update request
        updated_by: The user who made the update (for audit logging)
        
    Returns:
        Updated settings
    """
    # Load current settings
    current_settings = _load_settings_from_file()
    
    # Apply updates
    update_data = update_request.model_dump(exclude_unset=True)
    if update_data:
        updated_settings = current_settings.model_copy(update=update_data)
    else:
        updated_settings = current_settings
    
    # Update audit fields
    updated_settings.updated_at = datetime.now()
    if updated_by:
        updated_settings.updated_by = updated_by
    
    # Save to file
    _save_settings_to_file(updated_settings)
    
    # Log the change for audit purposes
    logger.info(f"Org settings updated by {updated_by or 'unknown'}: {update_data}")
    
    return updated_settings


def get_settings_audit_log() -> list:
    """
    Get audit log of settings changes.
    
    In a production environment, this would read from a proper audit log.
    For now, we'll return an empty list as the file-based storage doesn't
    support audit logging.
    """
    # In a real implementation, this would read from a database or log file
    # that tracks all settings changes
    return []