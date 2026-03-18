from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.api import deps
from app.models.wedding import Event, User
from app.schemas.event import EventCreate, EventResponse

router = APIRouter()

@router.post("/", response_model=EventResponse)
def create_event(
    event_in: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Crée un nouvel événement de mariage pour l'utilisateur connecté.
    """
    new_event = Event(
        **event_in.model_dump(),
        owner_id=current_user.id
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/", response_model=List[EventResponse])
def list_my_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Liste tous les mariages appartenant à l'utilisateur connecté.
    """
    return db.query(Event).filter(Event.owner_id == current_user.id).all()
