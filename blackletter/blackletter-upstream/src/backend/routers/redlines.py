from __future__ import annotations
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.redline import Redline

router = APIRouter()

class RedlineRequest(BaseModel):
    issueId: str
    text: str

@router.post("/redlines")
def save_redline(req: RedlineRequest, db: Session = Depends(get_db)):
    redline = Redline(issue_id=req.issueId, text=req.text)
    db.add(redline)
    db.commit()
    db.refresh(redline)
    return {"id": redline.id}
