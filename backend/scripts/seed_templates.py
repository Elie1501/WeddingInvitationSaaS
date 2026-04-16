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
                "default_config": {
                    "canvas": {"background_color": "#FDF5E6"},
                    "theme": {"primaryColor": "#451a03", "fontFamily": "Playfair Display"},
                    "elements": [
                        {"id": "names", "type": "text", "x": 0, "y": 1400, "width": 1080, "height": 200, "content": "{groom_name} & {bride_name}", "style": {"fontSize": "100px"}}
                    ]
                }
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
                "default_config": {
                    "canvas": {"background_color": "#FFFFFF"},
                    "theme": {"primaryColor": "#111827", "fontFamily": "Montserrat"},
                    "elements": [
                        {"id": "names", "type": "text", "x": 0, "y": 1400, "width": 1080, "height": 200, "content": "{groom_name} & {bride_name}", "style": {"fontSize": "100px"}}
                    ]
                }
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
                "default_config": {
                    "canvas": {"background_color": "#0c0a09"},
                    "theme": {"primaryColor": "#d4af37", "fontFamily": "Great Vibes"},
                    "elements": [
                        {"id": "names", "type": "text", "x": 0, "y": 1400, "width": 1080, "height": 200, "content": "{groom_name} & {bride_name}", "style": {"fontSize": "100px"}}
                    ]
                }
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
                "default_config": {
                    "canvas": {"background_color": "#fdf8f3"},
                    "theme": {"primaryColor": "#c46647", "fontFamily": "Playfair Display"},
                    "elements": [
                        {"id": "names", "type": "text", "x": 0, "y": 1400, "width": 1080, "height": 200, "content": "{groom_name} & {bride_name}", "style": {"fontSize": "100px"}}
                    ]
                }
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
                "default_config": {
                    "canvas": {"background_color": "#020617"},
                    "theme": {"primaryColor": "#f8fafc", "fontFamily": "Cormorant Garamond"},
                    "elements": [
                        {"id": "names", "type": "text", "x": 0, "y": 1400, "width": 1080, "height": 200, "content": "{groom_name} & {bride_name}", "style": {"fontSize": "100px"}}
                    ]
                }
            }),
            "thumbnail_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&q=80&w=800",
            "is_active": True
        },
        {
            "id": "floral-romance",
            "name": "🌸 Floral Romance",
            "description": "Un style doux et romantique avec des motifs floraux délicats.",
            "required_plan": "classic",
            "manifest_json": json.dumps({
                "default_config": {
                    "canvas": {"background_color": "#FFF5F7"},
                    "theme": {"primaryColor": "#4D2C2C", "fontFamily": "Playfair Display"},
                    "elements": [
                        {"id": "names", "type": "text", "x": 0, "y": 1400, "width": 1080, "height": 200, "content": "{groom_name} & {bride_name}", "style": {"fontSize": "100px"}}
                    ]
                }
            }),
            "thumbnail_url": "https://images.unsplash.com/photo-1522673607200-1648832cee98?auto=format&fit=crop&q=80&w=800",
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
