from fastapi.testclient import TestClient
from app.main import app
from app.tests.conftest import TestingSessionLocal
from app.models.wedding import User

client = TestClient(app)


def _signup_login(email: str, password: str = "password123") -> str:
    client.post("/auth/signup", json={"email": email, "password": password})
    resp = client.post("/auth/login", data={"username": email, "password": password})
    return resp.json()["access_token"]


def _make_admin(email: str) -> None:
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.is_admin = True
            db.commit()
    finally:
        db.close()


def _h(token: str):
    return {"Authorization": f"Bearer {token}"}


def test_admin_can_list_users():
    token = _signup_login("admin_ok@example.com")
    _make_admin("admin_ok@example.com")
    resp = client.get("/users/", headers=_h(token))
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_admin_can_read_stats():
    token = _signup_login("admin_stats@example.com")
    _make_admin("admin_stats@example.com")
    assert client.get("/users/stats", headers=_h(token)).status_code == 200


def test_regular_user_blocked_on_admin_routes():
    token = _signup_login("regular_user@example.com")  # is_admin reste False
    assert client.get("/users/", headers=_h(token)).status_code == 403
    assert client.get("/users/stats", headers=_h(token)).status_code == 403
    assert client.get("/users/1/cards", headers=_h(token)).status_code == 403
    assert client.patch("/users/1/status", json={"is_active": False}, headers=_h(token)).status_code == 403
    assert client.delete("/users/1", headers=_h(token)).status_code == 403


def test_anonymous_blocked_on_admin_routes():
    assert client.get("/users/").status_code == 401
    assert client.get("/users/stats").status_code == 401


def test_admin_cannot_delete_self():
    token = _signup_login("admin_self@example.com")
    _make_admin("admin_self@example.com")
    me = client.get("/auth/me", headers=_h(token)).json()
    resp = client.delete(f"/users/{me['id']}", headers=_h(token))
    assert resp.status_code == 400
