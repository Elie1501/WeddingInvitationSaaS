import os
import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base, get_db

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)


def signup_and_login(email: str, password: str = "password123") -> str:
    client.post("/auth/signup", json={"email": email, "password": password})
    resp = client.post("/auth/login", data={"username": email, "password": password})
    return resp.json()["access_token"]


def create_user_with_card(email: str) -> tuple:
    """Crée un user + un event (qui auto-crée une carte) et retourne (token, card_id)."""
    token = signup_and_login(email)
    client.post(
        "/events/",
        json={"title": "Mariage Test", "groom_name": "A", "bride_name": "B"},
        headers={"Authorization": f"Bearer {token}"}
    )
    cards = client.get("/cards/", headers={"Authorization": f"Bearer {token}"}).json()
    return token, cards[0]["id"]


# PUT /{card_id} — mise à jour OK
def test_update_card():
    token, card_id = create_user_with_card("card_user@example.com")
    # 2 pages + 1 cover existante = 3 = max → OK
    payload = {"intro_text": "Bienvenue !", "config_json": json.dumps({"pages": [{}, {}]})}
    response = client.put(
        f"/cards/{card_id}",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["intro_text"] == "Bienvenue !"


# PUT /{card_id} — dépasse la limite de pages (classic = 3 max) → 403
def test_update_card_exceeds_page_limit():
    token, card_id = create_user_with_card("card_limit@example.com")
    # 3 pages + 1 cover existante = 4 > 3 → 403
    payload = {"config_json": json.dumps({"pages": [{}, {}, {}]})}
    response = client.put(
        f"/cards/{card_id}",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


# POST /{card_id}/publish — publier puis dépublier
def test_publish_card():
    token, card_id = create_user_with_card("card_pub@example.com")

    # Premier appel → publie
    resp1 = client.post(
        f"/cards/{card_id}/publish",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp1.status_code == 200
    assert resp1.json()["is_published"] is True

    # Deuxième appel → dépublie
    resp2 = client.post(
        f"/cards/{card_id}/publish",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp2.status_code == 200
    assert resp2.json()["is_published"] is False


# GET /{card_id} — accès interdit si la carte n'appartient pas au user → 404
def test_get_card_not_owner():
    token_a, card_id = create_user_with_card("card_owner@example.com")
    token_b = signup_and_login("card_spy@example.com")

    response = client.get(
        f"/cards/{card_id}",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert response.status_code == 404
