from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import os
from app.db.session import engine, Base, SessionLocal
from app.api.api_v1.api import api_router
from app.models.wedding import CardTemplate, User
from app.core import security

# Création des tables
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    templates = [
        {
            "id": "ora-parallax",
            "name": "Élégance Parallaxe",
            "description": "Un design majestueux avec effet parallaxe, animation de pétales et typographie raffinée.",
            "thumbnail_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=400",
            "required_plan": "classic",
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
    ]

    for t_data in templates:
        existing = db.query(CardTemplate).filter(CardTemplate.id == t_data["id"]).first()
        manifest_json = json.dumps(t_data["default_config"])
        if existing:
            existing.name = t_data["name"]
            existing.description = t_data["description"]
            existing.thumbnail_url = t_data["thumbnail_url"]
            existing.required_plan = t_data["required_plan"]
            existing.manifest_json = manifest_json
            existing.is_active = True
        else:
            new_tpl = CardTemplate(
                id=t_data["id"],
                name=t_data["name"],
                description=t_data["description"],
                thumbnail_url=t_data["thumbnail_url"],
                required_plan=t_data["required_plan"],
                manifest_json=manifest_json,
                is_active=True
            )
            db.add(new_tpl)

    # Forcer l'activation de UNIQUEMENT ces templates, désactiver les autres
    allowed_ids = [t["id"] for t in templates]
    db.query(CardTemplate).filter(CardTemplate.id.in_(allowed_ids)).update({CardTemplate.is_active: True})
    db.query(CardTemplate).filter(~CardTemplate.id.in_(allowed_ids)).update({CardTemplate.is_active: False})
    db.commit()
    db.close()

seed_data()

app = FastAPI(title="API Mariage", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router)

if not os.path.exists("uploads"): os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def health_check(): return {"status": "online"}
