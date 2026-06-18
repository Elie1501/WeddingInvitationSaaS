from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.config import settings
from app.models.wedding import User
from app.schemas.token import TokenPayload
from app.api.plans import get_limits, has_paid_plan

from typing import Optional

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Un compte désactivé ne doit plus passer, même avec un token encore valide.
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Votre compte a été désactivé. Veuillez contacter l'administrateur.",
        )
    return user

def get_current_user_optional(
    db: Session = Depends(get_db), 
    token: Optional[str] = Depends(OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False))
) -> Optional[User]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
        user = db.query(User).filter(User.id == token_data.sub).first()
        return user
    except (JWTError, ValidationError):
        return None

def check_plan_permission(permission: str):
    def _check(current_user: User = Depends(get_current_user)):
        limits = get_limits(current_user.plan)
        if not limits.get(permission, False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Cette fonctionnalité nécessite un forfait supérieur (votre forfait actuel : {current_user.plan})"
            )
        return True
    return _check


def require_paid_plan(current_user: User = Depends(get_current_user)) -> User:
    """Dependency pour toute route exigeant un forfait payé (Classic ou Premium).

    Bloque les comptes fraîchement créés qui n'ont pas encore réglé leur forfait
    (paywall strict). Renvoie 402 Payment Required.
    """
    if not has_paid_plan(current_user.plan):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Veuillez choisir et régler un forfait pour accéder à cette fonctionnalité.",
        )
    return current_user


def require_premium(current_user: User = Depends(get_current_user)) -> User:
    """Dependency pour toute route réservée exclusivement au forfait Premium."""
    if current_user.plan != "premium":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cette fonctionnalité est réservée au forfait Premium."
        )
    return current_user
