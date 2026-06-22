from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.wedding import User, Card, Event
from app.schemas.user import UserResponse, UserUpdatePlan, UserUpdateStatus
from app.schemas.card import CardResponse
from app.api.deps import require_admin
import datetime

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
    current_user: User = Depends(require_admin)
):
    """
    Lister tous les utilisateurs (Réservé aux administrateurs).
    """
    users = db.query(User).all()
    return users

PLAN_PRICES = {"classic": 29.0, "premium": 79.0}

@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    now = datetime.datetime.utcnow()
    start_of_month = datetime.datetime(now.year, now.month, 1)

    # Utilisateurs actifs (hors admins)
    total_users = db.query(User).filter(User.is_admin == False, User.is_active == True).count()
    premium_users = db.query(User).filter(User.is_admin == False, User.is_active == True, User.plan == "premium").count()
    classic_users = db.query(User).filter(User.is_admin == False, User.is_active == True, User.plan == "classic").count()

    # Tous les users (actifs + inactifs) pour le churn
    all_users_count = db.query(User).filter(User.is_admin == False).count()
    inactive_users = db.query(User).filter(User.is_admin == False, User.is_active == False).count()

    # Nouveaux inscrits ce mois (pour MRR)
    new_this_month = db.query(User).filter(
        User.is_admin == False,
        User.created_at >= start_of_month
    ).all()
    new_premium_month = sum(1 for u in new_this_month if u.plan == "premium")
    new_classic_month = sum(1 for u in new_this_month if u.plan == "classic")

    # Cartes créées ce mois
    cards_this_month = db.query(Card).filter(Card.created_at >= start_of_month).count()

    # MRR = revenus des nouveaux inscrits ce mois
    mrr = round(new_premium_month * PLAN_PRICES["premium"] + new_classic_month * PLAN_PRICES["classic"], 2)
    # ARR = projection annuelle basée sur le MRR du mois
    arr = round(mrr * 12, 2)

    # Taux de conversion inscrits → payants (premium / total actifs)
    conversion_rate = round((premium_users / total_users * 100) if total_users > 0 else 0.0, 1)

    # Churn rate = % d'utilisateurs désactivés sur l'ensemble
    churn_rate = round((inactive_users / all_users_count * 100) if all_users_count > 0 else 0.0, 1)

    return {
        "total_users": total_users,
        "premium_users": premium_users,
        "classic_users": classic_users,
        "cards_this_month": cards_this_month,
        "new_users_this_month": len(new_this_month),
        "mrr": mrr,
        "arr": arr,
        "conversion_rate": conversion_rate,
        "churn_rate": churn_rate,
    }

@router.get("/{user_id}/cards", response_model=List[CardResponse])
def get_user_cards(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Lister toutes les cartes d'un utilisateur spécifique (Réservé aux administrateurs).
    """
    cards = db.query(Card).join(Event).filter(Event.owner_id == user_id).all()
    return [sign_media_urls(c) for c in cards]

@router.patch("/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    status_in: UserUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Activer ou désactiver un compte utilisateur (Réservé aux administrateurs).
    """
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
    current_user: User = Depends(require_admin)
):
    """
    Supprimer définitivement un utilisateur (Réservé aux administrateurs).
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    
    # Sécurité : ne pas se supprimer soi-même pour éviter de bloquer l'accès admin
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas supprimer votre propre compte admin.")

    db.delete(user)
    db.commit()
    return None

