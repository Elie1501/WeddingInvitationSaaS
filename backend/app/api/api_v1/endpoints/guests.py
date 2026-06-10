from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import datetime
import csv
import io
from app.db.session import get_db
from app.api import deps
from app.models.wedding import Guest, Event, User, Card, RSVP, guest_table_association
from app.schemas.guest import GuestCreate, GuestResponse, GuestRSVP, GuestUpdate, RSVPResponse, PublicRSVPCreate
from app.api.plans import get_limits

router = APIRouter()

# --- Private Endpoints ---

@router.get("/event/{event_id}", response_model=List[GuestResponse])
def list_guests(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    status: Optional[str] = None,
    q: Optional[str] = None,
    table_id: Optional[int] = None
):
    """Liste les invités d'un événement avec filtres optionnels (status, q, table_id)."""
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    query = db.query(Guest).filter(Guest.event_id == event_id)

    if status:
        query = query.filter(Guest.rsvp_status == status)

    if q:
        search = f"%{q.lower()}%"
        query = query.filter(
            (Guest.first_name.ilike(search)) | (Guest.last_name.ilike(search))
        )

    if table_id:
        query = query.join(guest_table_association, Guest.id == guest_table_association.c.guest_id).filter(
            guest_table_association.c.table_id == table_id
        )

    return query.order_by(Guest.id.asc()).all()

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

@router.patch("/{guest_id}", response_model=GuestResponse)
def update_guest(
    guest_id: int,
    guest_in: GuestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Modifie les informations d'un invité existant."""
    guest = db.query(Guest).join(Event).filter(Guest.id == guest_id, Event.owner_id == current_user.id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Invité non trouvé")

    update_data = guest_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(guest, field, value)

    db.commit()
    db.refresh(guest)
    return guest

@router.get("/event/{event_id}/rsvps", response_model=List[RSVPResponse])
def list_event_rsvps(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Retourne toutes les réponses RSVP enregistrées pour un événement."""
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    rsvps = (
        db.query(RSVP)
        .join(Guest, RSVP.guest_id == Guest.id)
        .filter(Guest.event_id == event_id)
        .order_by(RSVP.created_at.desc())
        .all()
    )
    return rsvps

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
    rsvp_data: PublicRSVPCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
):
    card = db.query(Card).filter(Card.event_id == rsvp_data.event_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Invitation non trouvée")

    is_owner = current_user and card.event.owner_id == current_user.id
    if not card.is_published and not is_owner:
        raise HTTPException(status_code=403, detail="L'invitation n'est pas encore publiée. Le RSVP n'est pas autorisé.")

    # Chercher ou créer l'invité principal
    guest = db.query(Guest).filter(
        Guest.event_id == rsvp_data.event_id,
        Guest.first_name == rsvp_data.first_name,
        Guest.last_name == rsvp_data.last_name
    ).first()

    if not guest:
        guest = Guest(
            event_id=rsvp_data.event_id,
            first_name=rsvp_data.first_name,
            last_name=rsvp_data.last_name,
            email=rsvp_data.email
        )
        db.add(guest)
        db.flush()

    guest.rsvp_status = "confirmed" if rsvp_data.presence else "declined"
    guest.dietary_restrictions = rsvp_data.dietary_restrictions
    guest.message = rsvp_data.message
    if rsvp_data.email:
        guest.email = rsvp_data.email

    # Recréer les sous-invités à chaque soumission
    db.query(Guest).filter(Guest.parent_id == guest.id).delete()

    if rsvp_data.presence:
        for sub in rsvp_data.sub_guests:
            db.add(Guest(
                event_id=rsvp_data.event_id,
                parent_id=guest.id,
                first_name=sub.first_name,
                last_name=sub.last_name,
                rsvp_status="confirmed",
                dietary_restrictions=sub.dietary_restrictions
            ))
    else:
        for table in guest.assigned_tables:
            table.remaining_seats += 1
        guest.assigned_tables = []

    rsvp_record = RSVP(
        guest_id=guest.id,
        presence=rsvp_data.presence,
        plus_ones=len(rsvp_data.sub_guests) if rsvp_data.presence else 0,
        dietary_restrictions=rsvp_data.dietary_restrictions,
        message=rsvp_data.message,
        created_at=datetime.datetime.utcnow()
    )
    db.add(rsvp_record)

    db.commit()
    return guest
