from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import os
from app.db.session import engine, Base, SessionLocal
from app.api.api_v1.api import api_router
from app.models.wedding import CardTemplate, User
from app.core import security

Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # On garde les templates actifs
    templates = [
        {
            "id": "arche-royale",
            "name": "L'Arche Royale",
            "description": "Une photo majestueuse découpée en arche dorée.",
            "thumbnail_url": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=600",
            "required_plan": "classic",
            "default_config": {
                "canvas": {"width": 1080, "height": 1920, "background_color": "#FDFBF7"},
                "theme": {"primaryColor": "#C5A059", "secondaryColor": "#FDFBF7", "fontFamily": "serif"},
                "elements": [
                    {"id": "hero_image", "type": "image", "x": 140, "y": 150, "width": 800, "height": 1100, "content": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=1000", "style": {"borderRadius": "400px 400px 0 0", "mask": "arch", "outline": "gold"}},
                    {"id": "names", "type": "text", "x": 0, "y": 1350, "width": 1080, "height": 200, "content": "{groom_name} & {bride_name}", "style": {"fontSize": "100px", "fontFamily": "serif", "color": "#1A1A1A", "fontStyle": "italic"}},
                    {"id": "date", "type": "text", "x": 0, "y": 1600, "width": 1080, "height": 100, "content": "{date}", "style": {"fontSize": "40px", "letterSpacing": "0.3em", "color": "#C5A059"}}
                ]
            }
        },
        {
            "id": "coeur-passion",
            "name": "Cœur Romantique",
            "description": "Votre amour au centre d'un cœur élégant.",
            "thumbnail_url": "https://images.unsplash.com/photo-1518133910546-b6c2fb7d79e3?w=600",
            "required_plan": "classic",
            "default_config": {
                "canvas": {"width": 1080, "height": 1920, "background_color": "#FFF5F5"},
                "theme": {"primaryColor": "#E53E3E", "secondaryColor": "#FFF5F5", "fontFamily": "serif"},
                "elements": [
                    {"id": "hero_image", "type": "image", "x": 140, "y": 300, "width": 800, "height": 800, "content": "https://images.unsplash.com/photo-1518133910546-b6c2fb7d79e3?w=1000", "style": {"borderRadius": "50%"}},
                    {"id": "c2", "type": "text", "x": 0, "y": 1200, "width": 1080, "height": 150, "content": "OUI POUR LA VIE", "style": {"fontSize": "30px", "letterSpacing": "0.5em", "color": "#E53E3E", "fontWeight": "bold"}},
                    {"id": "names", "type": "text", "x": 0, "y": 1350, "width": 1080, "height": 200, "content": "{groom_name} & {bride_name}", "style": {"fontSize": "90px", "fontFamily": "serif", "color": "#1A1A1A"}}
                ]
            }
        },
        {
            "id": "modern-chic",
            "name": "Modern Chic",
            "description": "Épuré, minimaliste et résolument moderne.",
            "thumbnail_url": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=600",
            "required_plan": "classic",
            "default_config": {
                "canvas": {"width": 1080, "height": 1920, "background_color": "#FFFFFF"},
                "theme": {"primaryColor": "#111827", "secondaryColor": "#FFFFFF", "fontFamily": "Montserrat"},
                "elements": [
                    {"id": "hero_image", "type": "image", "x": 0, "y": 0, "width": 1080, "height": 1200, "content": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=1200", "style": {"objectFit": "cover"}},
                    {"id": "names", "type": "text", "x": 80, "y": 1300, "width": 920, "height": 200, "content": "{groom_name}\n&\n{bride_name}", "style": {"fontSize": "80px", "textAlign": "left", "fontWeight": "900", "textTransform": "uppercase"}}
                ]
            }
        },
        {
            "id": "floral-romance",
            "name": "Floral Romance",
            "description": "Douceur florale et teintes poudrées.",
            "thumbnail_url": "https://images.unsplash.com/photo-1522673607200-1648832cee98?w=600",
            "required_plan": "classic",
            "default_config": {
                "canvas": {"width": 1080, "height": 1920, "background_color": "#FFF5F7"},
                "theme": {"primaryColor": "#4D2C2C", "secondaryColor": "#FFF5F7", "fontFamily": "Cormorant Garamond"},
                "elements": [
                    {"id": "hero_image", "type": "image", "x": 100, "y": 200, "width": 880, "height": 1000, "content": "https://images.unsplash.com/photo-1522673607200-1648832cee98?w=1000", "style": {"borderRadius": "20px"}},
                    {"id": "names", "type": "text", "x": 0, "y": 1300, "width": 1080, "height": 200, "content": "{groom_name} & {bride_name}", "style": {"fontSize": "110px", "fontFamily": "'Playfair Display'"}}
                ]
            }
        }
    ]
    
    # Désactiver les anciens
    db.query(CardTemplate).update({CardTemplate.is_active: False})

    for t_data in templates:
        existing = db.query(CardTemplate).filter(CardTemplate.id == t_data["id"]).first()
        manifest_json = json.dumps(t_data)
        if existing:
            existing.name = t_data["name"]
            existing.description = t_data["description"]
            existing.thumbnail_url = t_data["thumbnail_url"]
            existing.required_plan = t_data.get("required_plan", "classic")
            existing.manifest_json = manifest_json
            existing.is_active = True
        else:
            new_tpl = CardTemplate(
                id=t_data["id"],
                name=t_data["name"],
                description=t_data["description"],
                thumbnail_url=t_data["thumbnail_url"],
                required_plan=t_data.get("required_plan", "classic"),
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
