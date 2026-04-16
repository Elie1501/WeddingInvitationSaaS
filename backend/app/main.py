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
        },
        {
            "id": "es-template",
            "name": "Élégance Sophistiquée",
            "description": "Un design minimaliste et luxueux, parfait pour les mariages modernes.",
            "thumbnail_url": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=800",
            "required_plan": "premium",
            "default_config": {
                "layout": "es",
                "theme": {
                    "background": "#ffffff",
                    "accent": "#000000",
                    "text": "#1a1a1a",
                    "fontFamily": "Inter"
                },
                "sections": ["es-hero", "es-intro", "es-details", "es-footer"]
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
                "theme": {"background": "#FFF5F7", "accent": "#4D2C2C", "text": "#4D2C2C"}
            }
        },
        {
            "id": "classic-elegance",
            "name": "Classic Elegance",
            "description": "Style intemporel et épuré.",
            "thumbnail_url": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800",
            "required_plan": "classic",
            "default_config": {"layout": "arch", "theme": {"background": "#FDF5E6", "accent": "#451a03", "text": "#451a03"}}
        },
        {
            "id": "modern-chic",
            "name": "Modern Chic",
            "description": "Un design épuré et minimaliste pour les mariages urbains.",
            "thumbnail_url": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800",
            "required_plan": "classic",
            "default_config": {"layout": "typography-focus", "theme": {"background": "#FFFFFF", "accent": "#111827", "text": "#111827"}}
        },
        {
            "id": "bohemian-dream",
            "name": "🌿 Bohemian Dream (PREMIUM)",
            "description": "Un style nature, chaleureux et bohème pour un mariage en extérieur.",
            "thumbnail_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=800",
            "required_plan": "premium",
            "default_config": {"layout": "split", "theme": {"background": "#fdf8f3", "accent": "#c46647", "text": "#c46647"}}
        },
        {
            "id": "midnight-glamour",
            "name": "✨ Midnight Glamour (PREMIUM)",
            "description": "Sombre, mystérieux et intensément romantique.",
            "thumbnail_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=800",
            "required_plan": "premium",
            "default_config": {"layout": "arch", "theme": {"background": "#020617", "accent": "#f8fafc", "text": "#f8fafc"}}
        },
        {
            "id": "ey-aquarelle",
            "name": "EY - Aquarelle & Fleurs",
            "description": "Un design doux avec fond aquarelle, fleurs latérales et cartes superposées.",
            "thumbnail_url": "https://images.unsplash.com/photo-1508615070457-7baeba4003ab?w=800",
            "required_plan": "classic",
            "default_config": {
                "layout": "ey",
                "sections": ["ey-mairie", "ey-houppa", "program", "footer"],
                "theme": {
                    "background": "#fdf6f8",
                    "accent": "#8E4A5B",
                    "text": "#664A53",
                    "fontFamily": "Cinzel"
                },
                "content": {
                    "names": "Eden & Yaacov",
                    "hebrew_names": "עדן & יעקב",
                    "logo_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=200",
                    "mairie_title": "Cérémonie Civile",
                    "mairie_intro": "Se diront oui le",
                    "houppa_title": "Houppa & Soirée",
                    "houppa_announcement": "Ont la joie de vous faire part du mariage de leurs enfants",
                    "family_left": "M. et Mme\nHaim Trabelsi",
                    "family_right": "M. et Mme Fredy Elharrar\nMarcelle Levy",
                    "tsniout_text": "\"Une tenue Tsniout réjouira les mariés\"",
                    "remembrance_title": "À la mémoire de nos chers disparus",
                    "remembrance_left": "David et Eliane Elharrar ז׳׳ל\nRaphaël Levy ז׳׳ל",
                    "remembrance_right": "Eliahou et Borkana Trabelsi ז׳׳ל\nKhamous et Zoraya Haddad ז׳׳ל"
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
