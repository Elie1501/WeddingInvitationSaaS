from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.api import deps
from app.models.wedding import Guest, Event, User, Card
from app.schemas.guest import GuestCreate, GuestResponse, GuestRSVP

router = APIRouter()

@router.post("/", response_model=GuestResponse)
def add_guest(
    guest_in: GuestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Vérification : est-ce que l'événement appartient bien à l'utilisateur ?
    event = db.query(Event).filter(Event.id == guest_in.event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Vous n'êtes pas le propriétaire de cet événement")

    new_guest = Guest(**guest_in.model_dump())
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)
    return new_guest

@router.get("/event/{event_id}", response_model=List[GuestResponse])
def list_guests(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # On sécurise : on ne liste les invités que si on possède l'événement
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    return db.query(Guest).filter(Guest.event_id == event_id).all()


@router.patch("/rsvp/{guest_id}", response_model=GuestResponse)
def rsvp_guest(
    guest_id: int,
    rsvp_in: GuestRSVP,
    db: Session = Depends(get_db)
):
    # 1. On cherche l'invité
    guest = db.query(Guest).filter(Guest.id == guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Invité non trouvé")

    # 2. On vérifie si la carte de l'événement est bien publiée
    # On fait une jointure pour vérifier le statut de la Card liée à l'Event
    event_card = db.query(Card).filter(Card.event_id == guest.event_id).first()
    if not event_card or not event_card.is_published:
        raise HTTPException(
            status_code=400,
            detail="Le RSVP n'est pas encore ouvert pour cet événement"
        )

    # 3. Mise à jour des informations
    guest.rsvp_status = rsvp_in.rsvp_status
    guest.plus_ones = rsvp_in.plus_ones
    guest.dietary_restrictions = rsvp_in.dietary_restrictions

    db.commit()
    db.refresh(guest)
    return guest
