from fastapi import APIRouter, Depends, HTTPException, Response, Request
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
from app.core.csv_utils import csv_safe
from app.core.ratelimit import rate_limit

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

@router.get("/event/{event_id}/export/csv")
def export_guests_csv(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_export_csv"))
):
    """Exporte la liste des invités d'un événement en CSV (réservé Premium)."""
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    guests = db.query(Guest).filter(Guest.event_id == event_id).order_by(Guest.id.asc()).all()

    status_labels = {
        "confirmed": "Confirmé",
        "declined": "Décliné",
        "pending": "En attente",
    }

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow([
        "Prénom", "Nom", "Email", "Statut RSVP",
        "Accompagnants", "Régime alimentaire", "Table(s)", "Message",
    ])

    for g in guests:
        tables = ", ".join(t.name for t in g.assigned_tables) if g.assigned_tables else ""
        writer.writerow([
            csv_safe(g.first_name),
            csv_safe(g.last_name),
            csv_safe(g.email or ""),
            status_labels.get(g.rsvp_status, g.rsvp_status or ""),
            g.plus_ones or 0,
            csv_safe(g.dietary_restrictions or ""),
            csv_safe(tables),
            csv_safe(g.message or ""),
        ])

    # BOM UTF-8 pour que les accents s'affichent correctement dans Excel (FR).
    content = '﻿'.encode('utf-8') + output.getvalue().encode('utf-8')

    return Response(
        content=content,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename=invites_{event_id}.csv"}
    )

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
    request: Request,
    rsvp_data: PublicRSVPCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
):
    # Anti-spam : 15 soumissions / 5 min par IP.
    rate_limit(request, scope="rsvp", limit=15, window_seconds=300)

    card = db.query(Card).filter(Card.event_id == rsvp_data.event_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Invitation non trouvée")

    is_owner = current_user and card.event.owner_id == current_user.id
    if not card.is_published and not is_owner:
        raise HTTPException(status_code=403, detail="L'invitation n'est pas encore publiée. Le RSVP n'est pas autorisé.")

    # Chercher l'invité principal (jamais un sous-invité) par nom. Si un email est
    # fourni, on évite d'écraser un homonyme enregistré avec un AUTRE email :
    # on ne met à jour que l'invité au même email (ou sans email), sinon on en crée un.
    query = db.query(Guest).filter(
        Guest.event_id == rsvp_data.event_id,
        Guest.parent_id.is_(None),
        Guest.first_name == rsvp_data.first_name,
        Guest.last_name == rsvp_data.last_name,
    )
    if rsvp_data.email:
        query = query.filter(
            (Guest.email == rsvp_data.email) | (Guest.email.is_(None)) | (Guest.email == "")
        )
    guest = query.first()

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
