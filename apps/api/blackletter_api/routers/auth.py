from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from .. import database
from ..models import auth as auth_models
from ..services.auth_service import auth_service

router = APIRouter(
    prefix="/v1/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

# --- Pydantic Models for API data shapes ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    name: str | None

# --- API Endpoints ---
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(database.get_db)):
    # In a real implementation, this would also create a default Org and OrgMember.
    hashed_password = auth_service.get_password_hash(user.password)
    new_user = auth_models.User(email=user.email, password_hash=hashed_password, name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully. Please log in."}


@router.post("/login")
async def login(response: Response, user_credentials: UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(auth_models.User).filter(auth_models.User.email == user_credentials.email).first()

    if not user or not auth_service.verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create a session
    session_token = auth_service.create_session_token()
    expires_at = auth_service.get_session_expiry()

    # Find first org membership
    first_membership = db.query(auth_models.OrgMember).filter(auth_models.OrgMember.user_id == user.id).first()
    if not first_membership:
        raise HTTPException(status_code=403, detail="User has no organization membership.")

    new_session = auth_models.Session(
        session_token=session_token,
        user_id=user.id,
        org_id=first_membership.org_id,
        expires_at=expires_at,
    )
    db.add(new_session)
    db.commit()

    response.set_cookie(
        key="bl_sess",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="lax",
        expires=expires_at,
    )
    return {"message": "Login successful"}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("bl_sess")
    return {"message": "Logout successful"}
