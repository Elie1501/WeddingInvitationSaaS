import json
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


def create_user_with_card(email: str) -> tuple:
    token = signup_and_login(email)
    client.post(
        "/events/",
        json={"title": "Mariage Test", "groom_name": "A", "bride_name": "B"},
        headers={"Authorization": f"Bearer {token}"}
    )
    cards = client.get("/cards/", headers={"Authorization": f"Bearer {token}"}).json()
    return token, cards[0]["id"]


def test_update_card():
    token, card_id = create_user_with_card("card_user@example.com")
    payload = {"intro_text": "Bienvenue !", "config_json": json.dumps({"pages": [{}, {}]})}
    response = client.put(
        f"/cards/{card_id}",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["intro_text"] == "Bienvenue !"


def test_update_card_exceeds_page_limit():
    token, card_id = create_user_with_card("card_limit@example.com")
    payload = {"config_json": json.dumps({"pages": [{}, {}, {}]})}
    response = client.put(
        f"/cards/{card_id}",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_publish_card():
    token, card_id = create_user_with_card("card_pub@example.com")

    resp1 = client.post(f"/cards/{card_id}/publish", headers={"Authorization": f"Bearer {token}"})
    assert resp1.status_code == 200
    assert resp1.json()["is_published"] is True

    resp2 = client.post(f"/cards/{card_id}/publish", headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    assert resp2.json()["is_published"] is False


def test_get_card_not_owner():
    token_a, card_id = create_user_with_card("card_owner@example.com")
    token_b = signup_and_login("card_spy@example.com")

    response = client.get(
        f"/cards/{card_id}",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert response.status_code == 404
