from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.wedding import User
from app.schemas.user import UserResponse, UserUpdatePlan, UserUpdateStatus
from app.api.deps import get_current_user

from typing import List

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lister tous les utilisateurs (Réservé aux administrateurs).
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Vous n'avez pas les droits nécessaires pour accéder à cette ressource."
        )
    
    users = db.query(User).all()
    return users

@router.patch("/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    status_in: UserUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Activer ou désactiver un compte utilisateur (Réservé aux administrateurs).
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Vous n'avez pas les droits nécessaires."
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    
    # Empêcher de désactiver son propre compte admin
    if user.id == current_user.id and not status_in.is_active:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas désactiver votre propre compte.")

    user.is_active = status_in.is_active
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.patch("/me/plan", response_model=UserResponse)
def update_user_plan(
    plan_in: UserUpdatePlan,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mettre à jour le forfait de l'utilisateur.
    """
    if plan_in.plan not in ["classic", "premium"]:
        raise HTTPException(
            status_code=400,
            detail="Forfait invalide. Choisissez 'classic' ou 'premium'."
        )
    
    current_user.plan = plan_in.plan
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
