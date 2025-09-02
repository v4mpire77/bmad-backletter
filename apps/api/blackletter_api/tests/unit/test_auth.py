from fastapi.testclient import TestClient
import pytest

from apps.api.main import app
from apps.api.models.user import Base, SessionLocal, User, engine

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def create_user(email: str, password: str) -> None:
    db = SessionLocal()
    user = User(email=email)
    user.set_password(password)
    db.add(user)
    db.commit()
    db.close()


def test_login_success_sets_cookie():
    create_user("user@example.com", "secret")
    resp = client.post("/login", json={"email": "user@example.com", "password": "secret"})
    assert resp.status_code == 200
    assert resp.cookies.get("session") is not None


def test_login_failure_returns_401():
    create_user("user@example.com", "secret")
    resp = client.post("/login", json={"email": "user@example.com", "password": "wrong"})
    assert resp.status_code == 401
    assert resp.cookies.get("session") is None
