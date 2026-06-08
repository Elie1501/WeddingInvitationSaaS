from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import datetime
import csv
import io
from app.db.session import get_db
from app.api import deps
from app.models.wedding import Guest, Event, User, Card, RSVP, guest_table_association
from app.schemas.guest import GuestCreate, GuestResponse, GuestRSVP, GuestUpdate, RSVPResponse
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
    rsvp_data: dict, 
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
):
    event_id = rsvp_data.get("event_id")
    
    # On cherche la carte. 
    # Si l'utilisateur est le propriétaire, on autorise même si non publiée.
    # Sinon, elle doit être publiée.
    card = db.query(Card).filter(Card.event_id == event_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Invitation non trouvée")
        
    is_owner = current_user and card.event.owner_id == current_user.id
    
    if not card.is_published and not is_owner:
        raise HTTPException(status_code=403, detail="L'invitation n'est pas encore publiée. Le RSVP n'est pas autorisé.")

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

    # Gérer les sous-invités (enfants et adultes suppl.)
    # On supprime les anciens sous-invités pour repartir de zéro
    db.query(Guest).filter(Guest.parent_id == guest.id).delete()

    if rsvp_data.get("presence"):
        # Option 1: Liste explicite de sous-invités
        if rsvp_data.get("sub_guests"):
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
        
        # Option 2: Création basée sur les compteurs (Adultes et Enfants)
        else:
            # On accepte 'adults' (total) ou 'guests_count'/'plus_ones' (accompagnants)
            if "adults" in rsvp_data:
                adults_count = int(rsvp_data["adults"])
            elif "guests_count" in rsvp_data:
                adults_count = int(rsvp_data["guests_count"]) + 1
            elif "plus_ones" in rsvp_data:
                adults_count = int(rsvp_data["plus_ones"]) + 1
            else:
                adults_count = 1

            children_count = int(rsvp_data.get("children", 0))

            # On crée n-1 adultes (le premier est l'invité principal)
            for i in range(adults_count - 1):
                new_sub = Guest(
                    event_id=event_id,
                    parent_id=guest.id,
                    first_name=f"Accompagnant",
                    last_name=f"{i+1} de {guest.first_name}",
                    rsvp_status="confirmed"
                )
                db.add(new_sub)
            
            # On crée n enfants
            for i in range(children_count):
                new_sub = Guest(
                    event_id=event_id,
                    parent_id=guest.id,
                    first_name=f"Enfant",
                    last_name=f"{i+1} de {guest.first_name}",
                    rsvp_status="confirmed"
                )
                db.add(new_sub)

    # Si décliné, libérer place en table
    if not rsvp_data.get("presence"):
        for table in guest.assigned_tables:
            table.remaining_seats += 1
        guest.assigned_tables = []

    # Enregistrer la réponse RSVP dans l'historique
    rsvp_record = RSVP(
        guest_id=guest.id,
        presence=bool(rsvp_data.get("presence")),
        plus_ones=len(rsvp_data.get("sub_guests", [])) if rsvp_data.get("sub_guests") else max(0, int(rsvp_data.get("adults", 1)) - 1),
        dietary_restrictions=rsvp_data.get("dietary_restrictions"),
        message=rsvp_data.get("message"),
        created_at=datetime.datetime.utcnow()
    )
    db.add(rsvp_record)

    db.commit()
    return guest
