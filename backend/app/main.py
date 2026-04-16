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
    
    # PHILOSOPHIE : MOTEUR DE CONCEPTION DE TEMPLATES ROBUSTES
    # Simplicité, Structure Fixe, Rendu Premium.
    
    templates = [
        {
            "id": "eclat-eternel",
            "name": "L'Éclat Éternel",
            "description": "Arche minimaliste et typographie luxe. Le choix de l'élégance absolue.",
            "thumbnail_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200",
            "required_plan": "ultimate",
            "default_config": {
                "layout": "arch",
                "style": "premium",
                "theme": {
                    "background": "#F9F7F2",
                    "accent": "#C5A059",
                    "text": "#1A1A1A"
                },
                "content": {
                    "names": "{groom_name} & {bride_name}",
                    "date": "{date}",
                    "location": "{location}",
                    "message": "Nous nous réjouissons de célébrer ce jour sacré à vos côtés.",
                    "image_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200"
                }
            }
        },
        {
            "id": "vogue-minimal",
            "name": "Vogue Minimal",
            "description": "L'art du vide. Une typographie puissante pour un impact maximal.",
            "thumbnail_url": "https://images.unsplash.com/photo-1510076857177-7470076d4098?w=1200",
            "required_plan": "classic",
            "default_config": {
                "layout": "typography-focus",
                "style": "minimalist",
                "theme": {
                    "background": "#FFFFFF",
                    "accent": "#000000",
                    "text": "#000000"
                },
                "content": {
                    "names": "{groom_name} & {bride_name}",
                    "date": "{date}",
                    "location": "{location}",
                    "message": "OUI.",
                    "image_url": "https://images.unsplash.com/photo-1510076857177-7470076d4098?w=1200"
                }
            }
        },
        {
            "id": "boheme-chic",
            "name": "Bohème Chic",
            "description": "Naturel et poétique. Des teintes douces pour une union champêtre.",
            "thumbnail_url": "https://images.unsplash.com/photo-1522673607200-1648832cee98?w=1200",
            "required_plan": "classic",
            "default_config": {
                "layout": "split",
                "style": "boho",
                "theme": {
                    "background": "#FFF5F7",
                    "accent": "#4D2C2C",
                    "text": "#4D2C2C"
                },
                "content": {
                    "names": "{groom_name} & {bride_name}",
                    "date": "{date}",
                    "location": "{location}",
                    "message": "Au grand air, sous les fleurs de cerisier.",
                    "image_url": "https://images.unsplash.com/photo-1522673607200-1648832cee98?w=1200"
                }
            }
        }
    ]

    # Désactiver les anciens
    db.query(CardTemplate).update({CardTemplate.is_active: False})

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
