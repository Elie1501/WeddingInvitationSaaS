from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import uuid
import datetime
from app.db.session import get_db
from app.api import deps
from app.models.wedding import Card, CardVersion, Event, User, SubEvent
from app.schemas.card import CardResponse, CardUpdate, CardVersionResponse, CardCreate, SubEventCreate
from app.core import storage

from app.api.plans import get_limits

router = APIRouter()

def count_pages(card_update: CardUpdate, current_has_cover: bool) -> int:
    pages_count = 0
    if card_update.config_json:
        try:
            config = json.loads(card_update.config_json)
            pages_count = len(config.get("pages", []))
        except:
            pass
    
    has_cover = card_update.has_cover_page if card_update.has_cover_page is not None else current_has_cover
    return pages_count + (1 if has_cover else 0)

def sign_media_urls(card: Card) -> Card:
    """Remplace les clés S3 par des URLs signées pour l'affichage."""
    if card.media_url and not card.media_url.startswith("http"):
        card.media_url = storage.generate_signed_url(card.media_url)
    if card.music_url and not card.music_url.startswith("http"):
        card.music_url = storage.generate_signed_url(card.music_url)
    return card

def check_card_ownership(db: Session, card_id: int, user_id: int) -> Card:
    card = db.query(Card).join(Event).filter(Card.id == card_id, Event.owner_id == user_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Carte non trouvée ou accès non autorisé")
    return card

@router.get("/", response_model=List[CardResponse])
def list_cards(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Liste les cartes des événements de l'utilisateur."""
    cards = db.query(Card).join(Event).filter(Event.owner_id == current_user.id).all()
    return [sign_media_urls(c) for c in cards]

@router.post("/", response_model=CardResponse)
def create_card(
    card_in: CardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Crée une nouvelle carte pour un événement."""
    # Vérifier que l'événement appartient à l'utilisateur
    event = db.query(Event).filter(Event.id == card_in.event_id, Event.owner_id == current_user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Événement non trouvé")
    
    # Vérifier si une carte existe déjà pour cet événement
    existing_card = db.query(Card).filter(Card.event_id == card_in.event_id).first()
    if existing_card:
        raise HTTPException(status_code=400, detail="Une carte existe déjà pour cet événement")

    template_id = card_in.template_id or "default-modern"
    
    # Si un template est spécifié, on peut optionnellement charger sa config par défaut
    config_json = None
    template = db.query(CardTemplate).filter(CardTemplate.id == template_id).first()
    if template:
        manifest = json.loads(template.manifest_json)
        config_json = json.dumps(manifest.get("default_config", {}))

    card = Card(
        event_id=card_in.event_id,
        template_id=template_id,
        intro_text=card_in.intro_text,
        theme_color=card_in.theme_color,
        media_url=card_in.media_url,
        music_url=card_in.music_url,
        config_json=config_json,
        slug=f"wedding-{uuid.uuid4().hex[:8]}"
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card

@router.get("/{card_id}", response_model=CardResponse)
def get_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Récupère les détails d'une carte."""
    card = check_card_ownership(db, card_id, current_user.id)
    return sign_media_urls(card)

@router.get("/{card_id}/export")
def export_card_json(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Exporte la configuration de la carte en JSON."""
    card = check_card_ownership(db, card_id, current_user.id)
    export_data = {
        "intro_text": card.intro_text,
        "theme_color": card.theme_color,
        "media_url": card.media_url,
        "music_url": card.music_url,
        "config_json": json.loads(card.config_json) if card.config_json else {}
    }
    return export_data

@router.post("/{card_id}/import", response_model=CardResponse)
def import_card_json(
    card_id: int,
    import_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Importe une configuration JSON pour la carte."""
    card = check_card_ownership(db, card_id, current_user.id)
    
    if "intro_text" in import_data:
        card.intro_text = import_data["intro_text"]
    if "theme_color" in import_data:
        card.theme_color = import_data["theme_color"]
    if "media_url" in import_data:
        card.media_url = import_data["media_url"]
    if "music_url" in import_data:
        card.music_url = import_data["music_url"]
    if "config_json" in import_data:
        card.config_json = json.dumps(import_data["config_json"])
    
    card.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(card)
    return card

@router.put("/{card_id}/save", response_model=CardResponse)
def auto_save_card(
    card_id: int,
    card_in: CardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Sauvegarde rapide de la carte (auto-save)."""
    card = check_card_ownership(db, card_id, current_user.id)
    
    # Vérification des limites de pages
    limits = get_limits(current_user.plan)
    total_pages = count_pages(card_in, card.has_cover_page)
    if total_pages > limits["max_pages"]:
        raise HTTPException(
            status_code=403, 
            detail=f"Votre forfait {current_user.plan} est limité à {limits['max_pages']} page(s)."
        )

    update_data = card_in.model_dump(exclude_unset=True)
    
    # Gestion des sous-événements
    if "sub_events" in update_data:
        sub_events_data = update_data.pop("sub_events")
        db.query(SubEvent).filter(SubEvent.card_id == card.id).delete()
        for se_data in (sub_events_data or []):
            new_se = SubEvent(card_id=card.id, **se_data)
            db.add(new_se)

    # Gestion des champs d'événement
    event_fields = ["title", "groom_name", "bride_name", "date", "location"]
    for field in event_fields:
        if field in update_data:
            setattr(card.event, field, update_data.pop(field))

    for field, value in update_data.items():
        setattr(card, field, value)
    
    card.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(card)
    return card

@router.put("/{card_id}", response_model=CardResponse)
def update_card(
    card_id: int,
    card_in: CardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Met à jour une carte et crée une nouvelle version."""
    card = check_card_ownership(db, card_id, current_user.id)
    
    # Vérification des limites de pages
    limits = get_limits(current_user.plan)
    total_pages = count_pages(card_in, card.has_cover_page)
    if total_pages > limits["max_pages"]:
        raise HTTPException(
            status_code=403, 
            detail=f"Votre forfait {current_user.plan} est limité à {limits['max_pages']} page(s)."
        )

    # Sauvegarde de la version actuelle avant mise à jour
    old_content = {
        "intro_text": card.intro_text,
        "theme_color": card.theme_color,
        "has_cover_page": card.has_cover_page,
        "media_url": card.media_url,
        "music_url": card.music_url,
        "config_json": card.config_json,
        "sub_events": [{"title": se.title, "time": se.time, "location": se.location, "description": se.description} for se in card.sub_events]
    }
    
    version = CardVersion(
        card_id=card.id,
        version_number=card.current_version,
        content_json=json.dumps(old_content)
    )
    db.add(version)
    
    # Mise à jour des champs
    update_data = card_in.model_dump(exclude_unset=True)
    
    # Gestion des sous-événements
    if "sub_events" in update_data:
        sub_events_data = update_data.pop("sub_events")
        db.query(SubEvent).filter(SubEvent.card_id == card.id).delete()
        for se_data in (sub_events_data or []):
            new_se = SubEvent(card_id=card.id, **se_data)
            db.add(new_se)

    # Gestion des champs d'événement
    event_fields = ["title", "groom_name", "bride_name", "date", "location"]
    for field in event_fields:
        if field in update_data:
            setattr(card.event, field, update_data.pop(field))

    for field, value in update_data.items():
        setattr(card, field, value)
    
    card.current_version += 1
    card.updated_at = datetime.datetime.utcnow()
    
    db.commit()
    db.refresh(card)
    return card

@router.post("/{card_id}/publish", response_model=CardResponse)
def publish_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Publie ou dépublie une carte."""
    card = check_card_ownership(db, card_id, current_user.id)
    card.is_published = not card.is_published
    
    if card.is_published and not card.slug:
        card.slug = f"wedding-{uuid.uuid4().hex[:8]}"
        
    db.commit()
    db.refresh(card)
    return card

@router.get("/{card_id}/versions", response_model=List[CardVersionResponse])
def get_card_versions(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Récupère l'historique des versions d'une carte."""
    card = check_card_ownership(db, card_id, current_user.id)
    return db.query(CardVersion).filter(CardVersion.card_id == card.id).order_by(CardVersion.version_number.desc()).all()

@router.post("/{card_id}/rollback/{version_number}", response_model=CardResponse)
def rollback_card(
    card_id: int,
    version_number: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Restaure une version précédente de la carte."""
    card = check_card_ownership(db, card_id, current_user.id)
    version = db.query(CardVersion).filter(
        CardVersion.card_id == card.id, 
        CardVersion.version_number == version_number
    ).first()
    
    if not version:
        raise HTTPException(status_code=404, detail="Version non trouvée")
        
    content = json.loads(version.content_json)
    card.intro_text = content.get("intro_text")
    card.theme_color = content.get("theme_color")
    card.media_url = content.get("media_url")
    card.music_url = content.get("music_url")
    card.config_json = content.get("config_json")
    
    card.current_version += 1
    card.updated_at = datetime.datetime.utcnow()
    
    db.commit()
    db.refresh(card)
    return card

@router.post("/{card_id}/upload")
async def upload_media(
    card_id: int,
    file: UploadFile = File(...),
    file_type: str = Form("image"),
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_customize_extensively"))
):
    """Upload un fichier vers S3 avec optimisation."""
    card = check_card_ownership(db, card_id, current_user.id)
    
    # Vérification spécifique pour la musique
    if file_type == "music":
        limits = get_limits(current_user.plan)
        if not limits.get("can_upload_music"):
            raise HTTPException(
                status_code=403, 
                detail=f"Votre forfait {current_user.plan} ne permet pas d'uploader votre propre musique. Veuillez passer au forfait Premium."
            )

    file_content = await file.read()
    s3_key = await storage.upload_file_to_s3(
        file_content=file_content,
        folder=f"cards/{card_id}",
        filename=file.filename,
        content_type=file.content_type
    )
    
    # Retourne l'URL signée pour affichage immédiat
    signed_url = storage.generate_signed_url(s3_key)
    
    if file_type == "image":
        # On ne remplace media_url que si c'est explicitement pour ça, 
        # mais par défaut pour l'auto-save, on préfère que le frontend gère via config_json
        # On va quand même garder la compatibilité si c'est l'image principale
        if not card.media_url:
            card.media_url = signed_url
    elif file_type == "music":
        card.music_url = signed_url
        
    db.commit()
    
    return {"url": signed_url, "key": s3_key}

@router.delete("/{card_id}")
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """Supprime une carte."""
    card = check_card_ownership(db, card_id, current_user.id)
    db.delete(card)
    db.commit()
    return {"message": "Carte supprimée"}
