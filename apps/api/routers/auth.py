from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..models.user import SessionLocal, User
from apps.api.blackletter_api.services import session as session_service

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)) -> dict[str, str]:
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not user.verify_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = session_service.create_session_token(str(user.id))
    response.set_cookie("session", token, httponly=True)
    return {"message": "Logged in"}


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("session")
    return {"message": "Logged out"}
