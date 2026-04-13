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
            "id": "modern-chic",
            "name": "Modern Chic",
            "description": "Un design épuré et moderne pour votre mariage.",
            "required_plan": "premium",
            "manifest_json": json.dumps({
                "colors": ["#000000", "#FFFFFF", "#F0F0F0"],
                "fonts": ["Inter", "serif"],
                "sections": ["hero", "itinerary", "rsvp"]
            }),
            "is_active": True
        },
        {
            "id": "classic-elegance",
            "name": "Classic Elegance",
            "description": "L'élégance intemporelle pour une cérémonie traditionnelle.",
            "required_plan": "classic",
            "manifest_json": json.dumps({
                "colors": ["#FDF5E6", "#8B4513", "#DAA520"],
                "fonts": ["Playfair Display", "serif"],
                "sections": ["hero", "details", "rsvp"]
            }),
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
            print(f"Le template {template_data['name']} existe déjà.")
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_templates()
