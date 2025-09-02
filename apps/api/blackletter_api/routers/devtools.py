"""Development tools router - dev environment only."""
from __future__ import annotations

import os
from fastapi import APIRouter, HTTPException, Query
from typing import Dict

from ..services.evidence import build_window

# Only enable in development
router = APIRouter()

# Environment check - only enable if explicitly set
DEV_TOOLS_ENABLED = os.getenv("ENABLE_DEV_TOOLS", "false").lower() == "true"


@router.get("/analyses/{analysis_id}/window")
async def preview_evidence_window(
    analysis_id: str,
    start: int = Query(..., description="Start character position"),
    end: int = Query(..., description="End character position"), 
    n: int = Query(2, description="Number of sentences before/after")
) -> Dict:
    """
    Debug endpoint for Story 1.3 - Evidence Window Builder.
    Returns preview of evidence window (dev only).
    
    Args:
        analysis_id: Analysis ID
        start: Start character position
        end: End character position
        n: Number of sentences (default 2)
        
    Returns:
        Evidence window preview
    """
    if not DEV_TOOLS_ENABLED:
        raise HTTPException(
            status_code=404, 
            detail="Dev tools not available in this environment"
        )
    
    try:
        window = build_window(analysis_id, start, end, n)
        return {
            "analysis_id": analysis_id,
            "window": window,
            "debug_info": {
                "requested_span": f"{start}-{end}",
                "sentence_window": n,
                "environment": "development"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to build evidence window: {str(e)}"
        )


@router.get("/health")
async def devtools_health():
    """Health check for dev tools."""
    return {
        "status": "ok",
        "module": "devtools",
        "enabled": DEV_TOOLS_ENABLED
    }