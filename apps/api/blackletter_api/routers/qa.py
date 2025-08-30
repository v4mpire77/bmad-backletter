from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["qa"])


@router.get("/qa/status")
async def qa_status() -> dict[str, str]:
    """Check QA router status."""
    return {"status": "ok"}
