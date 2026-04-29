from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.wedding import CardTemplate, Base
from app.core.config import settings
import json

db_url = settings.DATABASE_URL
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_ora_template():
    db = SessionLocal()
    
    ora_manifest = {
        "name": "Élégance Parallaxe",
        "description": "Un design majestueux avec effet parallaxe, animation de pétales et typographie raffinée.",
        "style": "classic",
        "default_config": {
            "layout": "ora",
            "theme": {
                "background": "#ffffff",
                "accent": "#C5A059",
                "text": "#1a1a1a",
                "fontFamily": "Cormorant Garamond"
            },
            "content": {
                "names": "Ora & Samuel",
                "hebrew_names": "אורה & שמואל",
                "image_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200",
                "parallax_image_url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=1200",
                "family_left": {
                    "title": "Famille NABET",
                    "parents": "M. & Mme Carole et Moshé NABET"
                },
                "family_right": {
                    "title": "Famille ATTARD & ASCOLI",
                    "parents": "M. & Mme ATTARD et ASCOLI"
                },
                "tribute_title": "Une pensée très émue pour nos disparus",
                "tribute_text": "Liliane Ascoli, Alfred Ascoli, Georges Attard, Georgette Attard, et nos grands-parents Jean-Jacques Nabet et Jossiane Nabet.",
                "tribute_blessing": "Que leurs bénédictions illuminent notre vie."
            }
        }
    }

    template_id = "ora-parallax"
    
    existing = db.query(CardTemplate).filter(CardTemplate.id == template_id).first()
    if not existing:
        new_template = CardTemplate(
            id=template_id,
            name=ora_manifest["name"],
            description=ora_manifest["description"],
            thumbnail_url="https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=400",
            manifest_json=json.dumps(ora_manifest),
            is_active=True,
            required_plan="classic"
        )
        db.add(new_template)
        db.commit()
        print(f"Template '{template_id}' ajouté avec succès.")
    else:
        existing.manifest_json = json.dumps(ora_manifest)
        existing.is_active = True
        existing.required_plan = "classic"
        db.commit()
        print(f"Template '{template_id}' mis à jour et activé.")
    
    db.close()

if __name__ == "__main__":
    seed_ora_template()
