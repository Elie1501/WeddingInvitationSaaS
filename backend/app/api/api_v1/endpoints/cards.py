from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os
import uuid
import datetime
import re
import unicodedata
from app.db.session import get_db
from app.api import deps
from app.models.wedding import Card, CardVersion, CardTemplate, Event, User, SubEvent
from app.schemas.card import CardResponse, CardUpdate, CardVersionResponse, CardCreate, SubEventCreate
from app.core import storage

from app.api.plans import get_limits, PREMIUM_SECTION_IDS

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

def _enforce_plan_features(card_in: CardUpdate, user_plan: str) -> None:
    """Bloque les features Premium pour un utilisateur Classic, quelle que soit l'origine de la requête."""
    if user_plan == "premium":
        return

    if card_in.config_json is not None:
        try:
            cfg = json.loads(card_in.config_json)
            sections = cfg.get("sections", [])
            forbidden = sorted(s for s in sections if s in PREMIUM_SECTION_IDS)
            if forbidden:
                raise HTTPException(
                    status_code=403,
                    detail=f"Les blocs suivants sont réservés au forfait Premium : {', '.join(forbidden)}"
                )
        except HTTPException:
            raise
        except Exception:
            pass

    if card_in.music_url is not None:
        raise HTTPException(
            status_code=403,
            detail="La musique est réservée au forfait Premium."
        )


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

    # Vérification que l'utilisateur a accès au template demandé
    config_dict = {}
    template = db.query(CardTemplate).filter(CardTemplate.id == template_id).first()
    if template and getattr(template, "required_plan", None) == "premium" and current_user.plan != "premium":
        raise HTTPException(status_code=403, detail="Ce template est réservé au forfait Premium.")
    if template:
        manifest = json.loads(template.manifest_json)
        config_dict = manifest.get("default_config", {})
    
    names_display = f"{event.groom_name} & {event.bride_name}"
    config_dict["content"] = config_dict.get("content", {})
    config_dict["content"]["names"] = names_display
    config_dict["content"]["splash_title"] = names_display

    if event.groom_name and event.bride_name:
        config_dict["content"]["monogram"] = (
            f"{event.groom_name[0].upper()} & {event.bride_name[0].upper()}"
        )

    MONTHS_FR = ["", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                 "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    if event.date:
        d = event.date
        config_dict["content"]["date_display"] = f"{d.day} {MONTHS_FR[d.month]} {d.year}"

    if event.location:
        config_dict["content"]["address"] = event.location

    if "hebrew_names" in config_dict["content"]:
        config_dict["content"]["hebrew_names"] = ""

    card = Card(
        event_id=card_in.event_id,
        template_id=template_id,
        intro_text=card_in.intro_text,
        theme_color=card_in.theme_color,
        media_url=card_in.media_url,
        music_url=card_in.music_url,
        config_json=json.dumps(config_dict),
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
    limits = get_limits(current_user.plan)

    if "intro_text" in import_data:
        card.intro_text = import_data["intro_text"]
    if "theme_color" in import_data:
        card.theme_color = import_data["theme_color"]
    if "media_url" in import_data:
        card.media_url = import_data["media_url"]
    if "music_url" in import_data:
        if not limits.get("can_upload_music"):
            raise HTTPException(status_code=403, detail="L'import d'une musique est réservé au forfait Premium.")
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
    _enforce_plan_features(card_in, current_user.plan)

    if card_in.config_json is not None:
        limits = get_limits(current_user.plan)
        total_pages = count_pages(card_in, card.has_cover_page)
        if total_pages > limits["max_pages"]:
            raise HTTPException(
                status_code=403,
                detail=f"Votre forfait {current_user.plan} est limité à {limits['max_pages']} page(s)."
            )

    # Vérification du required_plan si le template change
    if card_in.template_id is not None and card_in.template_id != card.template_id:
        tpl = db.query(CardTemplate).filter(CardTemplate.id == card_in.template_id).first()
        if tpl and getattr(tpl, "required_plan", None) == "premium" and current_user.plan != "premium":
            raise HTTPException(status_code=403, detail="Ce template est réservé au forfait Premium.")

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
    _enforce_plan_features(card_in, current_user.plan)

    if card_in.config_json is not None:
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

# ── URL personnalisée (slug) — réservé Premium ────────────────────────────────
class SlugUpdate(BaseModel):
    slug: str

def slugify(value: str) -> str:
    """Transforme un texte en slug URL : minuscules, sans accents, tirets."""
    value = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-{2,}", "-", value)

@router.patch("/{card_id}/slug", response_model=CardResponse)
def update_card_slug(
    card_id: int,
    payload: SlugUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
    _permission = Depends(deps.check_plan_permission("can_custom_slug"))
):
    """Définit une URL personnalisée (ex: mariage-marie-jean), réservé Premium."""
    card = check_card_ownership(db, card_id, current_user.id)

    base = slugify(payload.slug)
    if len(base) < 3:
        raise HTTPException(status_code=422, detail="L'URL personnalisée doit contenir au moins 3 caractères valides.")
    base = base[:60]

    # Garantir l'unicité : suffixe court si déjà pris par une AUTRE carte.
    candidate = base
    suffix = 1
    while True:
        existing = db.query(Card).filter(Card.slug == candidate, Card.id != card.id).first()
        if not existing:
            break
        suffix += 1
        candidate = f"{base}-{suffix}"

    card.slug = candidate
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
):
    """Upload un fichier vers S3 avec optimisation."""
    limits = get_limits(current_user.plan)
    if file_type == "music":
        if not limits.get("can_upload_music"):
            raise HTTPException(status_code=403, detail="L'upload de musique est réservé au forfait Premium.")
    else:
        if not limits.get("can_customize_extensively"):
            raise HTTPException(status_code=403, detail="La personnalisation de médias n'est pas disponible avec votre forfait.")

    card = check_card_ownership(db, card_id, current_user.id)

    # ── Validation type + extension (SVG/HTML exclus : vecteur XSS via /uploads) ──
    if file_type == "music":
        allowed_types = {"audio/mpeg", "audio/mp3", "audio/aac", "audio/ogg",
                         "audio/wav", "audio/x-wav", "audio/mp4", "audio/x-m4a"}
        allowed_ext = {".mp3", ".aac", ".ogg", ".wav", ".m4a"}
        max_bytes = 20 * 1024 * 1024  # 20 Mo
    else:
        allowed_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}
        allowed_ext = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
        max_bytes = 10 * 1024 * 1024  # 10 Mo

    ext = os.path.splitext(file.filename or "")[1].lower()
    if (file.content_type or "") not in allowed_types or ext not in allowed_ext:
        raise HTTPException(
            status_code=415,
            detail="Type de fichier non autorisé. " +
                   ("Formats audio acceptés : MP3, AAC, OGG, WAV, M4A." if file_type == "music"
                    else "Formats image acceptés : JPG, PNG, WEBP, GIF."),
        )

    # ── Lecture en flux avec plafond de taille (évite de charger un énorme fichier) ──
    chunks, size = [], 0
    while True:
        chunk = await file.read(1024 * 1024)
        if not chunk:
            break
        size += len(chunk)
        if size > max_bytes:
            raise HTTPException(
                status_code=413,
                detail=f"Fichier trop volumineux (max {max_bytes // (1024 * 1024)} Mo).",
            )
        chunks.append(chunk)
    file_content = b"".join(chunks)

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
