from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RedlineRequest(BaseModel):
    issueId: str
    text: str

@router.post("/redlines")
def save_redline(req: RedlineRequest):
    # TODO: persist to DB; for now, echo success
    return {"status": "saved", "issueId": req.issueId, "length": len(req.text)}
