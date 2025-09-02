from datetime import datetime
from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .. import database
from ..models.auth import Session as SessionModel


class SessionClaims(BaseModel):
    session_token: str
    user_id: str
    organization_id: str


def require_session(
    bl_sess: str | None = Cookie(None),
    db: Session = Depends(database.get_db),
) -> SessionClaims:
    if bl_sess is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = (
        db.query(SessionModel)
        .filter(SessionModel.session_token == bl_sess)
        .first()
    )
    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid session")

    return SessionClaims(
        session_token=bl_sess,
        user_id=str(session.user_id),
        organization_id=str(session.org_id),
    )
