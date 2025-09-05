from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient

from apps.api.blackletter_api.main import app
from apps.api.blackletter_api import database
from apps.api.blackletter_api.models.auth import User, Session
from apps.api.blackletter_api.models.organization import Org, OrgMember


@pytest.fixture
def client(db_session_mock):
    app.dependency_overrides[database.get_db] = lambda: db_session_mock
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()


def test_list_and_switch_organization(client, db_session_mock) -> None:
    db = db_session_mock
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

    session = db.query(Session).filter_by(session_token="token123").first()
    assert str(session.org_id) == new_org_id

