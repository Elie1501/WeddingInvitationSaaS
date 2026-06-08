from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import BaseModel, ValidationError
from app.db.session import get_db
from app.core import security
from app.core.config import settings
from app.models.wedding import User
from app.schemas.user import UserCreate, UserResponse, GoogleLoginRequest
from app.schemas.token import Token, TokenPayload
from app.api.deps import get_current_user
import firebase_admin
from firebase_admin import auth as firebase_auth, credentials

import os

# Initialisation de Firebase Admin (une seule fois)
try:
    firebase_admin.get_app()
except ValueError:
    # On cherche le fichier de service account local
    service_account_path = "firebase-service-account.json"
    if os.path.exists(service_account_path):
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
    else:
        # Fallback sur les variables d'environnement par défaut
        firebase_admin.initialize_app()

router = APIRouter()

@router.post("/google", response_model=Token)
def google_login(request: GoogleLoginRequest, db: Session = Depends(get_db)):
    """
    Authentification via Google Firebase.
    Vérifie l'id_token, crée l'utilisateur si besoin et renvoie nos JWT.
    """
    try:
        # 1. Vérifier le token Firebase
        decoded_token = firebase_auth.verify_id_token(request.id_token)
        email = decoded_token.get("email")
        
        if not email:
            raise HTTPException(status_code=400, detail="Token Google invalide (email manquant).")

        # 2. Chercher ou créer l'utilisateur dans notre DB
        user = db.query(User).filter(User.email == email).first()
        is_new_user = False

        if not user:
            is_new_user = True
            user = User(
                email=email,
                hashed_password="google_auth_placeholder",
                plan="classic"
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # 3. Générer nos propres tokens JWT (le front utilisera ceux-là ensuite)
        return {
            "access_token": security.create_access_token(user.id),
            "refresh_token": security.create_refresh_token(user.id),
            "token_type": "bearer",
            "is_new_user": is_new_user,
        }
    except Exception as e:
        print(f"Erreur Google Auth: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Échec de l'authentification Google: {str(e)}",
        )

@router.post("/signup", response_model=UserResponse)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Création d'un nouveau compte utilisateur.
    """
    # Vérifier si l'utilisateur existe déjà
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="Cet email est déjà enregistré."
        )

    # Création de l'utilisateur avec mot de passe haché
    new_user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        plan="classic"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Connexion utilisateur et génération de tokens JWT.
    """
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Vérification du mot de passe (try/except pour les comptes Google sans mot de passe bcrypt)
    try:
        password_valid = security.verify_password(form_data.password, user.hashed_password)
    except Exception:
        password_valid = False

    if not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Votre compte a été désactivé. Veuillez contacter l'administrateur.",
        )

    return {
        "access_token": security.create_access_token(user.id),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }

class RefreshTokenBody(BaseModel):
    refresh_token: str

@router.post("/refresh-token", response_model=Token)
def refresh_token(body: RefreshTokenBody, db: Session = Depends(get_db)):
    """
    Renouveler l'access token à partir d'un refresh token valide.
    """
    try:
        payload = jwt.decode(
            body.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        if token_data.type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token type")
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalide ou expiré.",
        )

    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    return {
        "access_token": security.create_access_token(user.id),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Récupérer les informations de l'utilisateur connecté.
    """
    return current_user