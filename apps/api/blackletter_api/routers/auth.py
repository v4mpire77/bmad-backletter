from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from .. import database
from ..models import auth as auth_models
from ..services.auth_service import auth_service
from ..services.errors import ErrorCode, error_response

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
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register_user(user: UserCreate, db: Session = Depends(database.get_db)):
    existing_user = (
        db.query(auth_models.User).filter(auth_models.User.email == user.email).first()
    )
    if existing_user:
        return error_response(
            ErrorCode.EMAIL_ALREADY_REGISTERED, "Email already registered"
        )

    hashed_password = auth_service.get_password_hash(user.password)
    new_user = auth_models.User(
        email=user.email, password_hash=hashed_password, name=user.name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut(id=str(new_user.id), email=new_user.email, name=new_user.name)


@router.post("/login")
async def login(response: Response, user_credentials: UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(auth_models.User).filter(auth_models.User.email == user_credentials.email).first()

    if not user or not auth_service.verify_password(user_credentials.password, user.password_hash):
        return error_response(
            ErrorCode.INCORRECT_CREDENTIALS,
            "Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create a session
    session_token = auth_service.create_session_token()
    expires_at = auth_service.get_session_expiry()

    # Find first org membership
    first_membership = db.query(auth_models.OrgMember).filter(auth_models.OrgMember.user_id == user.id).first()
    if not first_membership:
        return error_response(
            ErrorCode.NO_ORG_MEMBERSHIP, "User has no organization membership."
        )

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
