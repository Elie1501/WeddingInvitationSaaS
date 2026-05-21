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
    token = signup_and_login(email)
    resp = client.post(
        "/events/",
        json={"title": "Mariage Test", "groom_name": "A", "bride_name": "B"},
        headers={"Authorization": f"Bearer {token}"}
    )
    return token, resp.json()["id"]


def add_guest(token: str, event_id: int, first_name: str = "Alice", last_name: str = "Test") -> int:
    resp = client.post(
        "/guests/",
        json={"event_id": event_id, "first_name": first_name, "last_name": last_name},
        headers={"Authorization": f"Bearer {token}"}
    )
    return resp.json()["id"]


def create_table(token: str, event_id: int, capacity: int) -> int:
    resp = client.post(
        "/tables/",
        json={"event_id": event_id, "name": "Table 1", "capacity": capacity},
        headers={"Authorization": f"Bearer {token}"}
    )
    return resp.json()["id"]


# POST /{table_id}/assign/{guest_id} — assigner un invité (OK)
def test_assign_guest_to_table():
    token, event_id = create_user_with_event("table_user@example.com")
    table_id = create_table(token, event_id, capacity=2)
    guest_id = add_guest(token, event_id)

    response = client.post(
        f"/tables/{table_id}/assign/{guest_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["remaining_seats"] == 1
    assert any(g["id"] == guest_id for g in data["guests"])


# POST /{table_id}/assign/{guest_id} — table pleine → 400
def test_assign_guest_table_full():
    token, event_id = create_user_with_event("table_full@example.com")
    table_id = create_table(token, event_id, capacity=1)

    # Premier invité occupe la seule place
    guest1_id = add_guest(token, event_id, "Alice", "Test")
    client.post(f"/tables/{table_id}/assign/{guest1_id}", headers={"Authorization": f"Bearer {token}"})

    # Deuxième invité → table pleine
    guest2_id = add_guest(token, event_id, "Bob", "Test")
    response = client.post(
        f"/tables/{table_id}/assign/{guest2_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "pleine" in response.json()["detail"]
