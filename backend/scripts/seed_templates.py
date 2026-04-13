from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.wedding import CardTemplate, Base
from app.core.config import settings
import json

# On utilise l'URL des settings
db_url = settings.DATABASE_URL

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_templates():
    db = SessionLocal()
    # Création des tables si elles n'existent pas
    Base.metadata.create_all(bind=engine)

    templates_to_create = [
        {
            "id": "classic-elegance",
            "name": "Classic Elegance",
            "description": "L'élégance intemporelle pour une cérémonie traditionnelle.",
            "required_plan": "classic",
            "manifest_json": json.dumps({
                "colors": {"background": "#FDF5E6", "text": "#451a03", "accent": "#8B4513"},
                "fonts": {"headings": "Playfair Display", "body": "Cormorant Garamond"},
                "sections": ["banner", "details", "rsvp"]
            }),
            "thumbnail_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&q=80&w=800",
            "is_active": True
        },
        {
            "id": "modern-chic",
            "name": "Modern Chic",
            "description": "Un design épuré et minimaliste pour les mariages urbains.",
            "required_plan": "classic",
            "manifest_json": json.dumps({
                "colors": {"background": "#FFFFFF", "text": "#111827", "accent": "#000000"},
                "fonts": {"headings": "Montserrat", "body": "Inter"},
                "sections": ["banner", "itinerary", "rsvp"]
            }),
            "thumbnail_url": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?auto=format&fit=crop&q=80&w=800",
            "is_active": True
        },
        {
            "id": "royal-gold",
            "name": "⚜️ Royal Gold (PREMIUM)",
            "description": "Luxe absolu avec des touches d'or et une typographie royale.",
            "required_plan": "premium",
            "manifest_json": json.dumps({
                "colors": {"background": "#0c0a09", "text": "#f5f5f4", "accent": "#d4af37"},
                "fonts": {"headings": "Great Vibes", "body": "Cormorant Garamond"},
                "sections": ["banner", "details", "itinerary", "rsvp"]
            }),
            "thumbnail_url": "https://images.unsplash.com/photo-1510076857177-7470076d4098?auto=format&fit=crop&q=80&w=800",
            "is_active": True
        },
        {
            "id": "bohemian-dream",
            "name": "🌿 Bohemian Dream (PREMIUM)",
            "description": "Un style nature, chaleureux et bohème pour un mariage en extérieur.",
            "required_plan": "premium",
            "manifest_json": json.dumps({
                "colors": {"background": "#fdf8f3", "text": "#4a3728", "accent": "#c46647"},
                "fonts": {"headings": "Playfair Display", "body": "Montserrat"},
                "sections": ["banner", "details", "itinerary", "rsvp"]
            }),
            "thumbnail_url": "https://unsplash.com/fr/photos/couple-de-jeunes-maries-sur-lile-se-mariant-a-terre-jbtbin3u0Xw",
            "is_active": True
        },
        {
            "id": "midnight-glamour",
            "name": "✨ Midnight Glamour (PREMIUM)",
            "description": "Sombre, mystérieux et intensément romantique.",
            "required_plan": "premium",
            "manifest_json": json.dumps({
                "colors": {"background": "#020617", "text": "#f8fafc", "accent": "#94a3b8"},
                "fonts": {"headings": "Cormorant Garamond", "body": "Inter"},
                "sections": ["banner", "itinerary", "rsvp"]
            }),
            "thumbnail_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&q=80&w=800",
            "is_active": True
        }
    ]

    for template_data in templates_to_create:
        template = db.query(CardTemplate).filter(CardTemplate.id == template_data["id"]).first()
        if not template:
            new_template = CardTemplate(**template_data)
            db.add(new_template)
            print(f"Template créé : {template_data['name']} ({template_data['id']})")
        else:
            # Mise à jour si déjà existant
            for key, value in template_data.items():
                setattr(template, key, value)
            print(f"Template mis à jour : {template_data['name']}")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_templates()
