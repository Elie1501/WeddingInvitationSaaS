from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

EVENT_PAYLOAD = {"title": "Mon Mariage", "groom_name": "Alice", "bride_name": "Bob"}


def signup_and_login(email: str, password: str = "password123") -> str:
    client.post("/auth/signup", json={"email": email, "password": password})
    resp = client.post("/auth/login", data={"username": email, "password": password})
    return resp.json()["access_token"]


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


def test_create_event_exceeds_plan_limit():
    token = signup_and_login("ev_user@example.com")
    response = client.post(
        "/events/",
        json={**EVENT_PAYLOAD, "title": "Mariage 2"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_list_my_events():
    token = signup_and_login("ev_user@example.com")
    response = client.get("/events/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert all(e["owner_id"] is not None for e in data)


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
