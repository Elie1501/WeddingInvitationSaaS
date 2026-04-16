from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
import json
from app.db.session import get_db
from app.api import deps
from app.models.wedding import Event, User, Card, CardTemplate
from app.schemas.event import EventCreate, EventResponse

from app.core import storage

from app.api.plans import PLAN_LIMITS, get_limits

router = APIRouter()

@router.post("/", response_model=EventResponse)
def create_event(
    event_in: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Crée un nouvel événement de mariage pour l'utilisateur connecté.
    Crée également une Card par défaut associée avec le template choisi.
    """
    # Vérifier la limite de sites (événements)
    limits = get_limits(current_user.plan)
    existing_events_count = db.query(Event).filter(Event.owner_id == current_user.id).count()
    if existing_events_count >= limits["max_sites"]:
        raise HTTPException(
            status_code=403, 
            detail=f"Votre forfait {current_user.plan} est limité à {limits['max_sites']} site(s)."
        )

    # On sépare les champs de personnalisation initiale
    event_data = event_in.model_dump()
    template_id = event_data.pop("template_id", "eclat-eternel")
    has_cp = event_data.pop("has_cover_page", True)
    has_cd = event_data.pop("has_countdown", True)

    new_event = Event(
        **event_data,
        owner_id=current_user.id
    )
    db.add(new_event)
    db.flush() 

    slug = f"wedding-{uuid.uuid4().hex[:8]}"

    # Charger la config du template par défaut et appliquer les choix
    config_dict = {}
    template = db.query(CardTemplate).filter(CardTemplate.id == template_id).first()
    if template:
        manifest = json.loads(template.manifest_json)
        config_dict = manifest.get("default_config", {})
    
    # Personnalisation initiale basée sur le formulaire
    config_dict["has_cover_page"] = has_cp
    config_dict["show_countdown_invitation"] = has_cd
    config_dict["show_countdown_splash"] = has_cd
    config_dict["content"] = config_dict.get("content", {})
    config_dict["content"]["splash_top_text"] = "Save the Date"
    config_dict["content"]["splash_button_text"] = "Ouvrir l'invitation"

    new_card = Card(
        event_id=new_event.id,
        template_id=template_id,
        slug=slug,
        intro_text=f"Bienvenue au mariage de {new_event.groom_name} & {new_event.bride_name} !",
        is_published=False,
        has_cover_page=has_cp,
        config_json=json.dumps(config_dict)
    )
    db.add(new_card)

    db.commit()
    db.refresh(new_event)
    return new_event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event_in: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Met à jour les informations d'un événement.
    """
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Événement non trouvé")

    update_data = event_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field != "template_id": # template_id est géré via Card
            setattr(event, field, value)

    db.commit()
    db.refresh(event)
    return event

@router.get("/public/card/{slug}")
def get_public_card(slug: str, db: Session = Depends(get_db)):
    card = db.query(Card).filter(Card.slug == slug, Card.is_published == True).first()
    if not card:
        raise HTTPException(status_code=404, detail="Invitation non trouvée ou non publiée")
    
    event = card.event
    
    # Signer les URLs si nécessaire
    media_url = card.media_url
    if media_url and not media_url.startswith("http"):
        media_url = storage.generate_signed_url(media_url)
    
    music_url = card.music_url
    if music_url and not music_url.startswith("http"):
        music_url = storage.generate_signed_url(music_url)

    limits = get_limits(event.owner.plan)

    return {
        "event_id": event.id,
        "title": event.title,
        "groom_name": event.groom_name,
        "bride_name": event.bride_name,
        "date": event.date,
        "location": event.location,
        "intro_text": card.intro_text,
        "theme_color": card.theme_color,
        "media_url": media_url,
        "music_url": music_url,
        "config_json": card.config_json,
        "template_id": card.template_id,
        "has_rsvp_form": limits.get("has_rsvp_form", False),
        "is_published": card.is_published,
        "sub_events": [{"title": se.title, "time": se.time, "location": se.location, "description": se.description} for se in card.sub_events]
    }

@router.get("/mine/latest")
def get_latest_event(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Récupère le dernier événement de l'utilisateur ou en crée un par défaut s'il n'en a pas.
    Utile pour rediriger directement vers l'éditeur après la connexion.
    """
    event = db.query(Event).filter(Event.owner_id == current_user.id).order_by(Event.id.desc()).first()
    
    if not event:
        # Créer un événement par défaut
        event = Event(
            title="Mon Mariage",
            groom_name="Marié",
            bride_name="Mariée",
            owner_id=current_user.id
        )
        db.add(event)
        db.flush()
        
        # Template par défaut: L'Éclat Éternel (Ultra-Simple)
        t_id = "eclat-eternel"
        template = db.query(CardTemplate).filter(CardTemplate.id == t_id).first()
        
        # Si le template n'existe pas encore, on prend le premier dispo
        if not template:
            template = db.query(CardTemplate).first()
            t_id = template.id if template else "eclat-eternel"

        config_dict = {}
        if template:
            manifest = json.loads(template.manifest_json)
            config_dict = manifest.get("default_config", {"canvas": {"width": 1080, "height": 1920, "background_color": "#ffffff"}, "elements": []})
        
        card = Card(
            event_id=event.id,
            template_id=t_id,
            slug=f"wedding-{uuid.uuid4().hex[:8]}",
            config_json=json.dumps(config_dict)
        )
        db.add(card)
        db.commit()
        db.refresh(event)

    card = db.query(Card).filter(Card.event_id == event.id).first()
    return {
        "event_id": event.id,
        "card_id": card.id if card else None
    }

@router.get("/", response_model=List[EventResponse])
def list_my_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Liste tous les mariages appartenant à l'utilisateur connecté.
    """
    return db.query(Event).filter(Event.owner_id == current_user.id).all()

@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Supprime un événement et tout ce qui lui est associé (Card, Guests, Tables, etc.).
    """
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Événement non trouvé")
    
    db.delete(event)
    db.commit()
    return {"message": "Événement supprimé avec succès"}

@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Récupère les détails d'un événement spécifique.
    """
    event = db.query(Event).filter(Event.id == event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Événement non trouvé")
    return event
