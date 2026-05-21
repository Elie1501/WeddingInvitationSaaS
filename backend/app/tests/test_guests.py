import os
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


def create_user_with_event(email: str):
    """Retourne (token, event_id)."""
    token = signup_and_login(email)
    resp = client.post(
        "/events/",
        json={"title": "Mariage Test", "groom_name": "A", "bride_name": "B"},
        headers={"Authorization": f"Bearer {token}"}
    )
    return token, resp.json()["id"]


def create_user_with_event_and_card(email: str):
    """Retourne (token, event_id, card_id)."""
    token, event_id = create_user_with_event(email)
    cards = client.get("/cards/", headers={"Authorization": f"Bearer {token}"}).json()
    return token, event_id, cards[0]["id"]


# POST / — ajouter un invité avec sous-invités (logique parent/enfant)
def test_add_guest_with_sub_guests():
    token, event_id = create_user_with_event("guest_user@example.com")
    payload = {
        "event_id": event_id,
        "first_name": "Jean",
        "last_name": "Dupont",
        "rsvp_status": "confirmed",
        "sub_guests": [
            {"first_name": "Marie", "last_name": "Dupont"},
            {"first_name": "Paul",  "last_name": "Dupont"}
        ]
    }
    response = client.post("/guests/", json=payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    parent = response.json()
    assert parent["first_name"] == "Jean"
    assert parent["rsvp_status"] == "confirmed"
    parent_id = parent["id"]

    # Vérifier les sous-invités via la liste : parent_id correct + même statut que le parent
    list_resp = client.get(f"/guests/event/{event_id}", headers={"Authorization": f"Bearer {token}"})
    assert list_resp.status_code == 200
    all_guests = list_resp.json()
    children = [g for g in all_guests if g["parent_id"] == parent_id]
    assert len(children) == 2
    assert {g["first_name"] for g in children} == {"Marie", "Paul"}
    assert all(g["rsvp_status"] == "confirmed" for g in children)


# POST /public/rsvp — RSVP sans auth (carte publiée) → confirmed + sous-invité créé
def test_public_rsvp_confirmed():
    token, event_id, card_id = create_user_with_event_and_card("rsvp_owner@example.com")

    # Publier la carte
    client.post(f"/cards/{card_id}/publish", headers={"Authorization": f"Bearer {token}"})

    # RSVP sans authentification
    response = client.post("/guests/public/rsvp", json={
        "event_id": event_id,
        "first_name": "Sophie",
        "last_name": "Martin",
        "email": "sophie@example.com",
        "presence": True,
        "dietary_restrictions": "végétarien",
        "sub_guests": [{"first_name": "Léa", "last_name": "Martin"}]
    })
    assert response.status_code == 200

    # Vérifier le statut et le sous-invité via la liste authentifiée
    all_guests = client.get(
        f"/guests/event/{event_id}", headers={"Authorization": f"Bearer {token}"}
    ).json()
    sophie = next(g for g in all_guests if g["first_name"] == "Sophie")
    assert sophie["rsvp_status"] == "confirmed"
    children = [g for g in all_guests if g["parent_id"] == sophie["id"]]
    assert len(children) == 1
    assert children[0]["first_name"] == "Léa"


# POST /public/rsvp — carte non publiée → 403
def test_public_rsvp_card_not_published():
    token, event_id = create_user_with_event("no_pub@example.com")
    # La carte auto-créée n'est pas publiée

    response = client.post("/guests/public/rsvp", json={
        "event_id": event_id,
        "first_name": "Test",
        "last_name": "User",
        "presence": True
    })
    assert response.status_code == 403
