from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def signup_and_login(email: str, password: str = "password123") -> str:
    from app.tests.conftest import activate_plan
    client.post("/auth/signup", json={"email": email, "password": password})
    resp = client.post("/auth/login", data={"username": email, "password": password})
    token = resp.json()["access_token"]
    activate_plan(token)  # paywall strict : on active un forfait pour les tests
    return token


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


def test_assign_guest_from_other_event_rejected():
    """Un invité ne peut être affecté qu'à une table du même événement (règle métier §4)."""
    from app.tests.conftest import activate_plan
    token = signup_and_login("table_cross_event@example.com")
    activate_plan(token, "premium")  # premium autorise plusieurs événements (max_sites=5)
    # Deux événements appartenant au même propriétaire
    ev_a = client.post("/events/", json={"title": "Mariage A", "groom_name": "A", "bride_name": "B"},
                       headers={"Authorization": f"Bearer {token}"}).json()["id"]
    ev_b = client.post("/events/", json={"title": "Mariage B", "groom_name": "C", "bride_name": "D"},
                       headers={"Authorization": f"Bearer {token}"}).json()["id"]

    table_a = create_table(token, ev_a, capacity=5)      # table de l'événement A
    guest_b = add_guest(token, ev_b, "Charlie", "Test")  # invité de l'événement B

    response = client.post(
        f"/tables/{table_a}/assign/{guest_b}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert "même événement" in response.json()["detail"]


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
