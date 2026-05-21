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

EVENT_PAYLOAD = {"title": "Mon Mariage", "groom_name": "Alice", "bride_name": "Bob"}


def signup_and_login(email: str, password: str = "password123") -> str:
    client.post("/auth/signup", json={"email": email, "password": password})
    resp = client.post("/auth/login", data={"username": email, "password": password})
    return resp.json()["access_token"]


# POST / — créer un événement (OK)
def test_create_event():
    token = signup_and_login("ev_user@example.com")
    response = client.post(
        "/events/",
        json=EVENT_PAYLOAD,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Mon Mariage"
    assert "id" in data


# POST / — dépasse la limite du forfait classic (max_sites=1) → 403
def test_create_event_exceeds_plan_limit():
    token = signup_and_login("ev_user@example.com")  # déjà 1 event créé ci-dessus
    response = client.post(
        "/events/",
        json={**EVENT_PAYLOAD, "title": "Mariage 2"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


# GET / — lister ses propres événements
def test_list_my_events():
    token = signup_and_login("ev_user@example.com")
    response = client.get("/events/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert all(e["owner_id"] is not None for e in data)


# DELETE /{event_id} — supprimer son propre événement (OK)
def test_delete_event():
    token = signup_and_login("ev_user@example.com")
    events = client.get("/events/", headers={"Authorization": f"Bearer {token}"}).json()
    event_id = events[0]["id"]

    response = client.delete(
        f"/events/{event_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Événement supprimé avec succès"


# DELETE /{event_id} — supprimer l'événement d'un autre user → 404
def test_delete_other_user_event():
    token_a = signup_and_login("ev_owner@example.com")
    create_resp = client.post(
        "/events/",
        json=EVENT_PAYLOAD,
        headers={"Authorization": f"Bearer {token_a}"}
    )
    event_id = create_resp.json()["id"]

    token_b = signup_and_login("ev_thief@example.com")
    response = client.delete(
        f"/events/{event_id}",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert response.status_code == 404
