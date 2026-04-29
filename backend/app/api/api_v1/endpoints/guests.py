from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import datetime
import csv
import io
from app.db.session import get_db
from app.api import deps
from app.models.wedding import Guest, Event, User, Card, RSVP
from app.schemas.guest import GuestCreate, GuestResponse, GuestRSVP
from app.api.plans import get_limits

router = APIRouter()

# --- Private Endpoints ---

@router.get("/event/{event_id}", response_model=List[GuestResponse])
def list_guests(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Liste tous les invités (parents et enfants) d'un événement."""
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    return db.query(Guest).filter(Guest.event_id == event_id).order_by(Guest.id.asc()).all()

@router.post("/", response_model=GuestResponse)
def add_guest(
    guest_in: GuestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Ajoute un invité principal et ses sous-invités."""
    event = db.query(Event).filter(Event.id == guest_in.event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    # Créer le guest principal
    main_guest = Guest(
        event_id=guest_in.event_id,
        first_name=guest_in.first_name,
        last_name=guest_in.last_name,
        email=guest_in.email,
        rsvp_status=guest_in.rsvp_status,
        dietary_restrictions=guest_in.dietary_restrictions,
        message=guest_in.message
    )
    db.add(main_guest)
    db.flush()

    # Créer les sous-invités
    if guest_in.sub_guests:
        for sub_data in guest_in.sub_guests:
            sub_guest = Guest(
                event_id=guest_in.event_id,
                parent_id=main_guest.id,
                first_name=sub_data.first_name,
                last_name=sub_data.last_name,
                rsvp_status=guest_in.rsvp_status, # Même statut que le parent par défaut
                dietary_restrictions=sub_data.dietary_restrictions
            )
            db.add(sub_guest)

    db.commit()
    db.refresh(main_guest)
    return main_guest

@router.delete("/{guest_id}")
def delete_guest(
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Supprime un invité. Si c'est un parent, supprime aussi les enfants."""
    guest = db.query(Guest).join(Event).filter(Guest.id == guest_id, Event.owner_id == current_user.id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Invité non trouvé")
    
    # Libérer la place en table
    for table in guest.assigned_tables:
        table.remaining_seats += 1
    
    db.delete(guest)
    db.commit()
    return {"message": "Invité supprimé"}

# --- Public Endpoints ---

@router.post("/public/rsvp") 
def public_rsvp(
    rsvp_data: dict, 
    db: Session = Depends(get_db)
):
    event_id = rsvp_data.get("event_id")
    card = db.query(Card).filter(Card.event_id == event_id, Card.is_published == True).first()
    if not card:
        raise HTTPException(status_code=403, detail="RSVP non autorisé")

    # Chercher ou créer l'invité principal
    guest = db.query(Guest).filter(
        Guest.event_id == event_id,
        Guest.first_name == rsvp_data.get("first_name"),
        Guest.last_name == rsvp_data.get("last_name")
    ).first()

    if not guest:
        guest = Guest(
            event_id=event_id,
            first_name=rsvp_data.get("first_name"),
            last_name=rsvp_data.get("last_name"),
            email=rsvp_data.get("email")
        )
        db.add(guest)
        db.flush()

    guest.rsvp_status = "confirmed" if rsvp_data.get("presence") else "declined"
    guest.dietary_restrictions = rsvp_data.get("dietary_restrictions")
    guest.message = rsvp_data.get("message")

    # Gérer les sous-invités (enfants)
    if rsvp_data.get("sub_guests"):
        # On supprime les anciens sous-invités pour simplifier l'update
        db.query(Guest).filter(Guest.parent_id == guest.id).delete()
        
        for sub in rsvp_data.get("sub_guests"):
            new_sub = Guest(
                event_id=event_id,
                parent_id=guest.id,
                first_name=sub.get("first_name"),
                last_name=sub.get("last_name"),
                rsvp_status=guest.rsvp_status,
                dietary_restrictions=sub.get("dietary_restrictions")
            )
            db.add(new_sub)

    # Si décliné, libérer place en table
    if not rsvp_data.get("presence"):
        for table in guest.assigned_tables:
            table.remaining_seats += 1
        guest.assigned_tables = []

    db.commit()
    return guest
