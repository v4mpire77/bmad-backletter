"""
Router for organization settings endpoints.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from ..models.schemas import OrgSettings, SettingsUpdateRequest
from ..services.settings import get_org_settings, update_org_settings

router = APIRouter(tags=["settings"])


@router.get("/admin/settings", response_model=OrgSettings)
async def get_settings():
    """
    Get organization-level settings.
    
    Returns:
        Current organization settings
    """
    try:
        settings = get_org_settings()
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve settings: {str(e)}")


@router.put("/admin/settings", response_model=OrgSettings)
async def update_settings(update_request: SettingsUpdateRequest):
    """
    Update organization-level settings.
    
    Args:
        update_request: Settings update request
        
    Returns:
        Updated organization settings
    """
    try:
        # In a real implementation, we would get the current user from the session
        # For now, we'll use "admin" as the default user
        updated_settings = update_org_settings(update_request, updated_by="admin")
        return updated_settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")


@router.get("/admin/settings/audit", response_model=list)
async def get_settings_audit_log():
    """
    Get audit log of settings changes.
    
    Returns:
        List of settings change events
    """
    # In a production implementation, this would return actual audit log entries
    # For now, we return an empty list as our file-based storage doesn't support audit logging
    return []