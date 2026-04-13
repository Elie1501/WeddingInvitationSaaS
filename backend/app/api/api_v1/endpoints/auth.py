from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import ValidationError
from app.db.session import get_db
from app.core import security
from app.core.config import settings
from app.models.wedding import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token, TokenPayload
from app.api.deps import get_current_user

router = APIRouter()

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
        plan=user_in.plan
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
    print(f"Tentative de connexion pour : {form_data.username}")
    # Vérifier l'utilisateur
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        print(f"Utilisateur non trouvé : {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not security.verify_password(form_data.password, user.hashed_password):
        print(f"Mot de passe incorrect pour : {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"Connexion réussie pour : {form_data.username}")
    # Générer les tokens JWT
    return {
        "access_token": security.create_access_token(user.id),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }

@router.post("/refresh-token", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Renouveler l'access token à partir d'un refresh token valide.
    """
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
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