"""Settings router for Story 5.1 - Org Settings (LLM/OCR/Retention)"""
from __future__ import annotations

import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session, sessionmaker

from ..models.entities import (
    OrgSetting,
    LLMProvider,
    RetentionPolicy,
    ComplianceMode,
)
from ..database import engine

logger = logging.getLogger(__name__)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter(prefix="/api/settings", tags=["settings"])


class OrgSettingsRequest(BaseModel):
    """Request model for updating organization settings."""
    llm_provider: str = "none"  # none|openai|anthropic|gemini
    llm_enabled: bool = True
    ocr_enabled: bool = False
    retention_policy: str = "none"  # none|30d|90d
    compliance_mode: str = "strict"  # strict|standard
    evidence_window: int = 2


class OrgSettingsResponse(BaseModel):
    """Response model for organization settings."""
    llm_provider: str
    llm_enabled: bool
    ocr_enabled: bool
    retention_policy: str
    compliance_mode: str
    evidence_window: int
    privacy_note: str
    cost_note: str
    updated_at: str


def get_db() -> Session:
    """Dependency for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/org", response_model=OrgSettingsResponse)
async def get_org_settings(db: Session = Depends(get_db)) -> OrgSettingsResponse:
    """
    Get organization settings for Story 5.1.
    
    Returns current LLM provider, OCR enabled status, and retention policy.
    """
    try:
        # Get settings for default org (MVP uses single org)
        settings = db.query(OrgSetting).first()
        
        if not settings:
            # Create default settings if none exist
            settings = OrgSetting(
                llm_provider=LLMProvider.none,
                llm_enabled=True,
                ocr_enabled=False,
                retention_policy=RetentionPolicy.none,
                compliance_mode=ComplianceMode.strict,
                evidence_window=2,
            )
            db.add(settings)
            db.commit()
            db.refresh(settings)
        
        return OrgSettingsResponse(
            llm_provider=settings.llm_provider.value,
            llm_enabled=settings.llm_enabled,
            ocr_enabled=settings.ocr_enabled,
            retention_policy=settings.retention_policy.value,
            compliance_mode=settings.compliance_mode.value,
            evidence_window=settings.evidence_window,
            privacy_note="Your file stays private. LLM is off by default. When enabled, only short snippets are sent.",
            cost_note="Enabling LLM features may incur additional costs based on token usage. Monitor usage in admin metrics.",
            updated_at=settings.updated_at.isoformat(),
        )
        
    except Exception as e:
        logger.error(f"Failed to get org settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve organization settings")


@router.put("/org", response_model=OrgSettingsResponse)
async def update_org_settings(
    settings_request: OrgSettingsRequest,
    db: Session = Depends(get_db)
) -> OrgSettingsResponse:
    """
    Update organization settings for Story 5.1.
    
    Admin can edit LLM provider, OCR enabled, and retention policy.
    Changes are audited via updated_at timestamp.
    """
    try:
        # Validate enum values
        try:
            llm_provider = LLMProvider(settings_request.llm_provider)
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid LLM provider. Must be one of: {[p.value for p in LLMProvider]}"
            )
        
        try:
            retention_policy = RetentionPolicy(settings_request.retention_policy)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid retention policy. Must be one of: {[p.value for p in RetentionPolicy]}"
            )
        try:
            compliance_mode = ComplianceMode(settings_request.compliance_mode)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid compliance mode. Must be one of: {[c.value for c in ComplianceMode]}",
            )

        if settings_request.evidence_window < 1:
            raise HTTPException(
                status_code=400, detail="evidence_window must be a positive integer"
            )

        if not settings_request.llm_enabled and llm_provider != LLMProvider.none:
            raise HTTPException(
                status_code=400,
                detail="LLM provider must be 'none' when llm_enabled is false",
            )

        # Get or create settings
        settings = db.query(OrgSetting).first()

        if settings:
            # Update existing settings
            settings.llm_provider = (
                llm_provider if settings_request.llm_enabled else LLMProvider.none
            )
            settings.llm_enabled = settings_request.llm_enabled
            settings.ocr_enabled = settings_request.ocr_enabled
            settings.retention_policy = retention_policy
            settings.compliance_mode = compliance_mode
            settings.evidence_window = settings_request.evidence_window
        else:
            # Create new settings
            settings = OrgSetting(
                llm_provider=llm_provider if settings_request.llm_enabled else LLMProvider.none,
                llm_enabled=settings_request.llm_enabled,
                ocr_enabled=settings_request.ocr_enabled,
                retention_policy=retention_policy,
                compliance_mode=compliance_mode,
                evidence_window=settings_request.evidence_window,
            )
            db.add(settings)
        
        db.commit()
        db.refresh(settings)
        
        logger.info(f"Updated org settings: LLM={llm_provider.value}, OCR={settings_request.ocr_enabled}, Retention={retention_policy.value}")
        
        return OrgSettingsResponse(
            llm_provider=settings.llm_provider.value,
            llm_enabled=settings.llm_enabled,
            ocr_enabled=settings.ocr_enabled,
            retention_policy=settings.retention_policy.value,
            compliance_mode=settings.compliance_mode.value,
            evidence_window=settings.evidence_window,
            privacy_note="Your file stays private. LLM is off by default. When enabled, only short snippets are sent.",
            cost_note="Enabling LLM features may incur additional costs based on token usage. Monitor usage in admin metrics.",
            updated_at=settings.updated_at.isoformat(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update org settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to update organization settings")


@router.get("/org/privacy-impact")
async def get_privacy_impact(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get privacy impact information based on current settings.
    
    Provides transparency about data handling based on configuration.
    """
    try:
        settings = db.query(OrgSetting).first()

        if not settings:
            settings = OrgSetting()  # Use defaults
        
        privacy_impact = {
            "llm_data_sharing": {
                "enabled": settings.llm_enabled and settings.llm_provider != LLMProvider.none,
                "provider": settings.llm_provider.value,
                "data_shared": "Short text snippets only (max 220 tokens)" if settings.llm_enabled and settings.llm_provider != LLMProvider.none else "No data shared",
                "retention_by_provider": "Varies by provider - see their privacy policy" if settings.llm_enabled and settings.llm_provider != LLMProvider.none else "N/A"
            },
            "ocr_processing": {
                "enabled": settings.ocr_enabled,
                "data_processed": "Document images converted to text locally" if settings.ocr_enabled else "No OCR processing",
                "external_services": False  # Assuming local OCR
            },
            "data_retention": {
                "policy": settings.retention_policy.value,
                "description": {
                    "none": "Data retained indefinitely",
                    "30d": "Data automatically deleted after 30 days",
                    "90d": "Data automatically deleted after 90 days"
                }.get(settings.retention_policy.value, "Unknown policy"),
                "user_control": "You can delete individual analyses at any time"
            },
            "compliance_notes": [
                "All processing occurs on your chosen infrastructure",
                "Original documents are never shared with LLM providers",
                "PII redaction is applied before any external LLM calls",
                "You maintain full control over your data retention policy"
            ]
        }
        
        return privacy_impact
        
    except Exception as e:
        logger.error(f"Failed to get privacy impact: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve privacy impact information")


@router.get("/health")
async def settings_health() -> Dict[str, str]:
    """Health check for settings service."""
    return {
        "status": "ok",
        "module": "settings",
        "version": "1.0.0"
    }
