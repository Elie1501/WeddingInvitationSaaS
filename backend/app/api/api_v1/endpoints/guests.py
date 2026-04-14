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

# --- Private Endpoints (Back-office) ---

@router.get("/event/{event_id}", response_model=List[GuestResponse])
def list_guests(
    event_id: int,
    rsvp_status: Optional[str] = None,
    table_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Liste tous les invités d'un événement avec options de filtrage."""
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    query = db.query(Guest).filter(Guest.event_id == event_id)

    if rsvp_status:
        query = query.filter(Guest.rsvp_status == rsvp_status)
    
    if table_id:
        query = query.join(Guest.assigned_tables).filter(WeddingTable.id == table_id)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Guest.first_name.ilike(search_filter)) | 
            (Guest.last_name.ilike(search_filter)) |
            (Guest.email.ilike(search_filter))
        )

    return query.order_by(Guest.created_at.desc()).all()

@router.get("/event/{event_id}/summary")
def get_event_summary(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Fournit un résumé statistique des réponses pour un événement."""
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    guests = db.query(Guest).filter(Guest.event_id == event_id).all()
    
    summary = {
        "total_guests": len(guests),
        "confirmed": sum(1 for g in guests if g.rsvp_status == "confirmed"),
        "declined": sum(1 for g in guests if g.rsvp_status == "declined"),
        "pending": sum(1 for g in guests if g.rsvp_status == "pending"),
        "total_plus_ones": sum(g.plus_ones for g in guests if g.rsvp_status == "confirmed"),
        "total_expected": sum(1 + g.plus_ones for g in guests if g.rsvp_status == "confirmed")
    }
    
    return summary

@router.post("/", response_model=GuestResponse)
def add_guest(
    guest_in: GuestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Ajoute manuellement un invité."""
    event = db.query(Event).filter(Event.id == guest_in.event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=403, detail="Accès refusé")

    # Vérification des limites du plan
    limits = get_limits(current_user.plan)
    guest_count = db.query(Guest).filter(Guest.event_id == guest_in.event_id).count()
    if guest_count >= limits["max_guests"]:
        raise HTTPException(
            status_code=403, 
            detail=f"Limite d'invités atteinte pour votre forfait {current_user.plan} ({limits['max_guests']} max)"
        )

    new_guest = Guest(**guest_in.model_dump())
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)
    return new_guest

@router.delete("/{guest_id}")
def delete_guest(
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Supprime un invité et libère ses places dans les tables."""
    guest = db.query(Guest).join(Event).filter(Guest.id == guest_id, Event.owner_id == current_user.id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Invité non trouvé")
    
    # Libérer les places dans les tables avant suppression
    seats_to_free = 1 + (guest.plus_ones or 0)
    for table in guest.assigned_tables:
        table.remaining_seats += seats_to_free
    
    db.delete(guest)
    db.commit()
    return {"message": "Invité supprimé"}

@router.post("/event/{event_id}/import/csv")
async def import_guests_csv(
    event_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_import_export"))
):
    """Importe des invités à partir d'un fichier CSV."""
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Événement non trouvé")

    content = await file.read()
    decoded = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))
    
    limits = get_limits(current_user.plan)
    current_count = db.query(Guest).filter(Guest.event_id == event_id).count()
    
    new_guests = []
    for row in reader:
        if current_count >= limits["max_guests"]:
            break
            
        first_name = row.get("first_name") or row.get("prenom")
        last_name = row.get("last_name") or row.get("nom")
        email = row.get("email")
        
        if first_name and last_name:
            guest = Guest(
                event_id=event_id,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            db.add(guest)
            new_guests.append(guest)
            current_count += 1
            
    db.commit()
    return {"message": f"{len(new_guests)} invités importés avec succès."}

# --- Public Endpoints (Sans auth) ---

@router.post("/public/rsvp/{card_id}")
def public_rsvp_by_id(
    card_id: int,
    rsvp_in: GuestRSVP,
    first_name: str,
    last_name: str,
    email: str = None,
    db: Session = Depends(get_db)
):
    """Collecte un RSVP via l'ID de la carte."""
    card = db.query(Card).filter(Card.id == card_id, Card.is_published == True).first()
    if not card:
        raise HTTPException(status_code=404, detail="Invitation non trouvée ou non publiée")
    
    # Vérifier si le forfait autorise le formulaire RSVP
    limits = get_limits(card.event.owner.plan)
    if not limits.get("has_rsvp_form"):
        raise HTTPException(status_code=403, detail="Le formulaire RSVP n'est pas disponible pour ce forfait.")

    guest_count = db.query(Guest).filter(Guest.event_id == card.event_id).count()
    # Si c'est un nouvel invité et qu'on a atteint la limite
    existing = db.query(Guest).filter(
        Guest.event_id == card.event_id,
        Guest.first_name == first_name,
        Guest.last_name == last_name
    ).first()
    
    if not existing and guest_count >= limits["max_guests"]:
        raise HTTPException(status_code=403, detail="Cet événement ne peut plus recevoir de nouvelles confirmations (limite atteinte).")

    return process_rsvp(db, card.event_id, first_name, last_name, email, rsvp_in)

@router.post("/public/rsvp") # Compatible avec l'ancienne version slug-based
def public_rsvp_legacy(
    rsvp_data: dict, # On accepte un dictionnaire flexible
    db: Session = Depends(get_db)
):
    """Endpoint flexible pour PublicCardView.vue avec vérification de publication."""
    event_id = rsvp_data.get("event_id")
    if not event_id:
        raise HTTPException(status_code=400, detail="event_id manquant")
    
    # CONTRAINTE MÉTIER : Vérifier si la carte est publiée
    card = db.query(Card).filter(Card.event_id == event_id, Card.is_published == True).first()
    if not card:
        raise HTTPException(status_code=403, detail="Le RSVP est désactivé (carte non publiée).")

    event = card.event
    limits = get_limits(event.owner.plan)
    if not limits.get("has_rsvp_form"):
        raise HTTPException(status_code=403, detail="Le formulaire RSVP n'est pas disponible pour ce forfait.")

    guest_count = db.query(Guest).filter(Guest.event_id == event_id).count()
    
    existing = db.query(Guest).filter(
        Guest.event_id == event_id,
        Guest.first_name == rsvp_data.get("first_name"),
        Guest.last_name == rsvp_data.get("last_name")
    ).first()

    if not existing and guest_count >= limits["max_guests"]:
        raise HTTPException(status_code=403, detail="Limite d'invités atteinte pour cet événement.")

    rsvp_in = GuestRSVP(
        presence=rsvp_data.get("presence", True), 
        plus_ones=rsvp_data.get("plus_ones", 0),
        dietary_restrictions=rsvp_data.get("dietary_restrictions"),
        message=rsvp_data.get("message")
    )
    
    return process_rsvp(
        db, 
        event_id, 
        rsvp_data.get("first_name"), 
        rsvp_data.get("last_name"), 
        rsvp_data.get("email"), 
        rsvp_in
    )

def process_rsvp(db: Session, event_id: int, first_name: str, last_name: str, email: str, rsvp_in: GuestRSVP):
    # Chercher l'invité
    guest = db.query(Guest).filter(
        Guest.event_id == event_id,
        Guest.first_name == first_name,
        Guest.last_name == last_name
    ).first()

    if not guest:
        guest = Guest(
            event_id=event_id,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        db.add(guest)
        db.flush()

    # Mettre à jour le statut et synchroniser les tables
    old_plus_ones = guest.plus_ones or 0
    new_plus_ones = rsvp_in.plus_ones or 0
    diff = new_plus_ones - old_plus_ones

    guest.rsvp_status = "confirmed" if rsvp_in.presence else "declined"
    guest.plus_ones = new_plus_ones
    guest.dietary_restrictions = rsvp_in.dietary_restrictions
    guest.message = rsvp_in.message

    # Si l'invité décline, on le retire de ses tables
    if not rsvp_in.presence:
        for table in guest.assigned_tables:
            table.remaining_seats += (1 + old_plus_ones)
        guest.assigned_tables = []
    elif diff != 0:
        # Si le nombre d'accompagnants change, on ajuste les places restantes
        for table in guest.assigned_tables:
            table.remaining_seats -= diff

    # Créer une entrée dans l'historique RSVP
    new_rsvp = RSVP(
        guest_id=guest.id,
        presence=rsvp_in.presence,
        plus_ones=rsvp_in.plus_ones,
        dietary_restrictions=rsvp_in.dietary_restrictions,
        message=rsvp_in.message
    )
    db.add(new_rsvp)
    
    db.commit()
    db.refresh(guest)
    return guest
