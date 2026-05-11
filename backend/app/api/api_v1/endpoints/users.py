from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.wedding import User, Card, Event
from app.schemas.user import UserResponse, UserUpdatePlan, UserUpdateStatus
from app.schemas.card import CardResponse
from app.api.deps import get_current_user

from typing import List

router = APIRouter()

def sign_media_urls(card: Card) -> Card:
    """Remplace les clés S3 par des URLs signées pour l'affichage."""
    from app.core import storage
    if card.media_url and not card.media_url.startswith("http"):
        card.media_url = storage.generate_signed_url(card.media_url)
    if card.music_url and not card.music_url.startswith("http"):
        card.music_url = storage.generate_signed_url(card.music_url)
    return card

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

@router.get("/{user_id}/cards", response_model=List[CardResponse])
def get_user_cards(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lister toutes les cartes d'un utilisateur spécifique (Réservé aux administrateurs).
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Vous n'avez pas les droits nécessaires."
        )
    
    cards = db.query(Card).join(Event).filter(Event.owner_id == user_id).all()
    return [sign_media_urls(c) for c in cards]

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
    
    user.is_active = status_in.is_active
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Supprimer définitivement un utilisateur (Réservé aux administrateurs).
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Vous n'avez pas les droits nécessaires.")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    
    # Sécurité : ne pas se supprimer soi-même pour éviter de bloquer l'accès admin
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas supprimer votre propre compte admin.")

    db.delete(user)
    db.commit()
    return None

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
