from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_signup():
    response = client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "id" in response.json()


def test_signup_already_exists():
    response = client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cet email est déjà enregistré."


def test_login():
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_incorrect_password():
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Email ou mot de passe incorrect."


def test_me():
    login_response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_me_without_token():
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_refresh_token():
    login_response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    refresh_token = login_response.json()["refresh_token"]

    response = client.post(
        "/auth/refresh-token",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
