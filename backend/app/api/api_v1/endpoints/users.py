from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.wedding import User
from app.schemas.user import UserResponse, UserUpdatePlan
from app.api.deps import get_current_user

router = APIRouter()

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
