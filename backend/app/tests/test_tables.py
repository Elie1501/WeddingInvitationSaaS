from fastapi.testclient import TestClient
from app.main import app

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


def test_assign_guest_table_full():
    token, event_id = create_user_with_event("table_full@example.com")
    table_id = create_table(token, event_id, capacity=1)

    guest1_id = add_guest(token, event_id, "Alice", "Test")
    client.post(f"/tables/{table_id}/assign/{guest1_id}", headers={"Authorization": f"Bearer {token}"})

    guest2_id = add_guest(token, event_id, "Bob", "Test")
    response = client.post(
        f"/tables/{table_id}/assign/{guest2_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "pleine" in response.json()["detail"]
