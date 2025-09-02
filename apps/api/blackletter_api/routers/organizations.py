from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .. import database
from ..models.organization import Org, OrgMember
from ..models.auth import Session as SessionModel
from ..services.session import SessionClaims, require_session


router = APIRouter(prefix="/v1/organizations", tags=["Organizations"])


class OrgOut(BaseModel):
    id: str
    name: str
    slug: str | None = None


class SwitchOrgRequest(BaseModel):
    org_id: str


@router.get("/", response_model=list[OrgOut])
def list_user_organizations(
    claims: SessionClaims = Depends(require_session),
    db: Session = Depends(database.get_db),
) -> list[OrgOut]:
    orgs = (
        db.query(Org)
        .join(OrgMember, Org.id == OrgMember.org_id)
        .filter(OrgMember.user_id == claims.user_id)
        .all()
    )
    return [OrgOut(id=str(o.id), name=o.name, slug=o.slug) for o in orgs]


@router.post("/switch")
def switch_organization(
    request: SwitchOrgRequest,
    claims: SessionClaims = Depends(require_session),
    db: Session = Depends(database.get_db),
) -> dict[str, str]:
    membership = (
        db.query(OrgMember)
        .filter(OrgMember.user_id == claims.user_id, OrgMember.org_id == request.org_id)
        .first()
    )
    if not membership:
        raise HTTPException(status_code=403, detail="User not a member of organization")

    session = (
        db.query(SessionModel)
        .filter(SessionModel.session_token == claims.session_token)
        .first()
    )
    session.org_id = request.org_id
    db.commit()

    return {"organization_id": request.org_id}

