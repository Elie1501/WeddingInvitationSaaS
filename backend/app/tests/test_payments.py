"""Tests du gating forfait et des endpoints de paiement Stripe."""
import json
from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def signup_and_login(email: str, password: str = "password123") -> str:
    client.post("/auth/signup", json={"email": email, "password": password})
    resp = client.post("/auth/login", data={"username": email, "password": password})
    token = resp.json()["access_token"]
    # Paywall strict : on part d'un forfait Classic actif pour les tests de gating.
    set_user_plan(get_user_id(token), "classic")
    return token


def create_card_for_user(token: str) -> int:
    client.post(
        "/events/",
        json={"title": "Mariage Test", "groom_name": "A", "bride_name": "B"},
        headers={"Authorization": f"Bearer {token}"},
    )
    cards = client.get("/cards/", headers={"Authorization": f"Bearer {token}"}).json()
    return cards[0]["id"]


def get_user_id(token: str) -> int:
    from jose import jwt
    from app.core.config import settings
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return int(payload["sub"])


def set_user_plan(user_id: int, plan: str) -> None:
    from app.tests.conftest import TestingSessionLocal
    from app.models.wedding import User
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.plan = plan
            db.commit()
    finally:
        db.close()


# ─── Gating : blocs premium ───────────────────────────────────────────────────

def test_classic_cannot_save_countdown_block():
    token = signup_and_login("plan_countdown@example.com")
    card_id = create_card_for_user(token)

    config = json.dumps({"sections": ["hero", "countdown", "footer"]})
    resp = client.put(
        f"/cards/{card_id}/save",
        json={"config_json": config},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403
    assert "Premium" in resp.json()["detail"]


def test_classic_cannot_save_program_block():
    token = signup_and_login("plan_program@example.com")
    card_id = create_card_for_user(token)

    config = json.dumps({"sections": ["hero", "program"]})
    resp = client.put(
        f"/cards/{card_id}/save",
        json={"config_json": config},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403
    assert "program" in resp.json()["detail"]


def test_classic_can_save_classic_sections():
    token = signup_and_login("classic_sections_ok@example.com")
    card_id = create_card_for_user(token)

    config = json.dumps({"sections": ["hero", "rsvp", "footer"]})
    resp = client.put(
        f"/cards/{card_id}/save",
        json={"config_json": config},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200


def test_premium_can_save_premium_block():
    token = signup_and_login("premium_countdown@example.com")
    user_id = get_user_id(token)
    card_id = create_card_for_user(token)
    set_user_plan(user_id, "premium")

    config = json.dumps({"sections": ["hero", "countdown", "image", "footer"]})
    resp = client.put(
        f"/cards/{card_id}/save",
        json={"config_json": config},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200


# ─── Gating : musique ─────────────────────────────────────────────────────────

def test_classic_cannot_set_music_url():
    token = signup_and_login("music_block@example.com")
    card_id = create_card_for_user(token)

    resp = client.put(
        f"/cards/{card_id}/save",
        json={"music_url": "https://example.com/song.mp3"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403
    assert "Premium" in resp.json()["detail"]


def test_classic_cannot_set_music_url_via_update():
    token = signup_and_login("music_block_update@example.com")
    card_id = create_card_for_user(token)

    resp = client.put(
        f"/cards/{card_id}",
        json={"music_url": "https://example.com/song.mp3"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403


# ─── Gating : CSV export ──────────────────────────────────────────────────────

def test_csv_export_blocked_for_classic():
    token = signup_and_login("csv_gating@example.com")
    client.post(
        "/events/",
        json={"title": "Mariage T", "groom_name": "X", "bride_name": "Y"},
        headers={"Authorization": f"Bearer {token}"},
    )
    events = client.get("/events/", headers={"Authorization": f"Bearer {token}"}).json()
    event_id = events[0]["id"]

    resp = client.get(
        f"/tables/event/{event_id}/export/csv",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403


def test_csv_export_allowed_for_premium():
    token = signup_and_login("csv_premium@example.com")
    user_id = get_user_id(token)
    set_user_plan(user_id, "premium")

    client.post(
        "/events/",
        json={"title": "Mariage P", "groom_name": "X", "bride_name": "Y"},
        headers={"Authorization": f"Bearer {token}"},
    )
    events = client.get("/events/", headers={"Authorization": f"Bearer {token}"}).json()
    event_id = events[0]["id"]

    resp = client.get(
        f"/tables/event/{event_id}/export/csv",
        headers={"Authorization": f"Bearer {token}"},
    )
    # 200 même si aucune table (fichier CSV vide)
    assert resp.status_code == 200


# ─── Upgrade session Stripe ───────────────────────────────────────────────────

@patch("stripe.checkout.Session.create")
def test_create_upgrade_session_returns_checkout_url(mock_create):
    mock_session = MagicMock()
    mock_session.url = "https://checkout.stripe.com/pay/test_upgrade_123"
    mock_create.return_value = mock_session

    token = signup_and_login("upgrade_classic@example.com")
    resp = client.post(
        "/payments/create-upgrade-session",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["checkout_url"] == "https://checkout.stripe.com/pay/test_upgrade_123"
    assert data["amount"] == 5000  # 50,00 € en centimes


@patch("stripe.checkout.Session.create")
def test_upgrade_session_already_premium_returns_400(mock_create):
    token = signup_and_login("upgrade_already_premium@example.com")
    user_id = get_user_id(token)
    set_user_plan(user_id, "premium")

    resp = client.post(
        "/payments/create-upgrade-session",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 400
    assert "Premium" in resp.json()["detail"]
    mock_create.assert_not_called()


# ─── Webhook Stripe ───────────────────────────────────────────────────────────

@patch("stripe.Webhook.construct_event")
def test_webhook_updates_user_plan(mock_construct):
    token = signup_and_login("webhook_plan@example.com")
    user_id = get_user_id(token)

    mock_construct.return_value = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "payment_status": "paid",
                "metadata": {"user_id": str(user_id), "plan": "premium"},
            }
        },
    }

    resp = client.post(
        "/payments/webhook",
        content=b'{"test": "payload"}',
        headers={"stripe-signature": "t=1,v1=fakesig", "content-type": "application/json"},
    )
    assert resp.status_code == 200

    # Vérifier que le plan a bien été mis à jour
    from app.tests.conftest import TestingSessionLocal
    from app.models.wedding import User
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        assert user.plan == "premium"
    finally:
        db.close()


@patch("stripe.Webhook.construct_event")
def test_webhook_invalid_signature_returns_400(mock_construct):
    import stripe
    mock_construct.side_effect = stripe.error.SignatureVerificationError("bad sig", "sig_header")

    resp = client.post(
        "/payments/webhook",
        content=b'{"test": "bad"}',
        headers={"stripe-signature": "invalid", "content-type": "application/json"},
    )
    assert resp.status_code == 400
