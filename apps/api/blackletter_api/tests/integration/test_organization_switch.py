from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from apps.api.blackletter_api.main import app
from apps.api.blackletter_api import database
from apps.api.blackletter_api.models.auth import User, Session
from apps.api.blackletter_api.models.organization import Org, OrgMember

client = TestClient(app)


def setup_module(_: object) -> None:
    db = database.SessionLocal()
    try:
        db.query(Session).delete()
        db.query(OrgMember).delete()
        db.query(Org).delete()
        db.query(User).delete()
        db.commit()

        user = User(email="user@example.com", password_hash="hash")
        db.add(user)
        db.commit()
        db.refresh(user)

        org1 = Org(name="Org 1", slug="org1")
        org2 = Org(name="Org 2", slug="org2")
        db.add_all([org1, org2])
        db.commit()
        db.refresh(org1)
        db.refresh(org2)

        db.add_all([
            OrgMember(org_id=org1.id, user_id=user.id),
            OrgMember(org_id=org2.id, user_id=user.id),
        ])
        session = Session(
            session_token="token123",
            user_id=user.id,
            org_id=org1.id,
            expires_at=datetime.utcnow() + timedelta(days=1),
        )
        db.add(session)
        db.commit()
    finally:
        db.close()


def test_list_and_switch_organization() -> None:
    cookies = {"bl_sess": "token123"}

    resp = client.get("/api/v1/organizations", cookies=cookies)
    assert resp.status_code == 200
    orgs = resp.json()
    assert len(orgs) == 2

    new_org_id = orgs[1]["id"]
    resp = client.post(
        "/api/v1/organizations/switch",
        json={"org_id": new_org_id},
        cookies=cookies,
    )
    assert resp.status_code == 200
    assert resp.json()["organization_id"] == new_org_id

    db = database.SessionLocal()
    try:
        session = db.query(Session).filter_by(session_token="token123").first()
        assert str(session.org_id) == new_org_id
    finally:
        db.close()

