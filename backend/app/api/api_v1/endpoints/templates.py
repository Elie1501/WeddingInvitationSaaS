from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.wedding import CardTemplate
from app.schemas.card import TemplateResponse

router = APIRouter()

@router.get("/", response_model=List[TemplateResponse])
def list_templates(db: Session = Depends(get_db)):
    """Liste tous les templates disponibles et actifs."""
    return db.query(CardTemplate).filter(CardTemplate.is_active == True).all()

@router.get("/{template_id}", response_model=TemplateResponse)
def get_template(template_id: str, db: Session = Depends(get_db)):
    """Récupère un template spécifique."""
    template = db.query(CardTemplate).filter(CardTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template non trouvé")
    return template
