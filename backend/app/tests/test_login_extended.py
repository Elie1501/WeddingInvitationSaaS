from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base, get_db
import pytest

# Base de données de test (SQLite en mémoire)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_login.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
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

def test_signup_flow():
    """Test complet du flux d'inscription"""
    response = client.post(
        "/auth/signup",
        json={"email": "newuser@example.com", "password": "securepassword123", "plan": "premium"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["plan"] == "premium"

def test_login_success():
    """Test de connexion réussie"""
    response = client.post(
        "/auth/login",
        data={"username": "newuser@example.com", "password": "securepassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    """Test de connexion avec mauvais mot de passe (vérifie ma correction)"""
    response = client.post(
        "/auth/login",
        data={"username": "newuser@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Email ou mot de passe incorrect."

def test_login_user_not_found():
    """Test de connexion avec email inexistant"""
    response = client.post(
        "/auth/login",
        data={"username": "nonexistent@example.com", "password": "somepassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Email ou mot de passe incorrect."

def test_access_protected_route():
    """Test d'accès à une route protégée (/me)"""
    # 1. Login pour avoir le token
    login_res = client.post(
        "/auth/login",
        data={"username": "newuser@example.com", "password": "securepassword123"}
    )
    token = login_res.json()["access_token"]

    # 2. Accès avec token
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "newuser@example.com"

def test_access_protected_route_invalid_token():
    """Test d'accès avec un token bidon"""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer fake_token_here"}
    )
    # Le backend renvoie 403 (Forbidden) dans deps.py pour les tokens invalides
    assert response.status_code == 403

def test_refresh_token_flow():
    """Test du renouvellement de token"""
    # 1. Login
    login_res = client.post(
        "/auth/login",
        data={"username": "newuser@example.com", "password": "securepassword123"}
    )
    refresh_token = login_res.json()["refresh_token"]

    # 2. Refresh
    response = client.post(
        f"/auth/refresh-token?refresh_token={refresh_token}"
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    
def test_refresh_token_invalid():
    """Test refresh avec un token invalide"""
    response = client.post(
        "/auth/refresh-token?refresh_token=invalid_refresh_token"
    )
    assert response.status_code == 401
