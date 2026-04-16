import json
import os
import sys
import uuid

# Ajouter le chemin du projet pour importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.wedding import CardTemplate

def seed_ultimate_minimal():
    db = SessionLocal()
    
    # Template: L'Arche d'Or
    t_id = "template-arche-or"
    t_data = {
        "id": t_id,
        "name": "L'Arche d'Or",
        "description": "Design ultra-épuré avec photo en arche et finitions dorées.",
        "required_plan": "classic",
        "thumbnail_url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=400",
        "default_config": {
            "canvas": { "width": 1080, "height": 1920, "background_color": "#FCF9F5" },
            "elements": [
                {
                    "id": "hero_image",
                    "type": "image",
                    "x": 140, "y": 180, "width": 800, "height": 1050,
                    "content": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=1080",
                    "style": { "mask": "arch", "outline": "gold", "objectFit": "cover" }
                },
                {
                    "id": "names",
                    "type": "text",
                    "x": 40, "y": 1300, "width": 1000, "height": 180,
                    "content": "{groom_name} & {bride_name}",
                    "style": { "fontSize": 110, "fontFamily": "'Playfair Display', serif", "textAlign": "center", "color": "#1A1A1A" }
                },
                {
                    "id": "date",
                    "type": "text",
                    "x": 40, "y": 1550, "width": 1000, "height": 80,
                    "content": "{date}",
                    "style": { "fontSize": 34, "fontFamily": "Inter, sans-serif", "textAlign": "center", "color": "#4A4A4A", "letterSpacing": "8px", "textTransform": "uppercase" }
                },
                {
                    "id": "location",
                    "type": "text",
                    "x": 40, "y": 1650, "width": 1000, "height": 60,
                    "content": "{location}",
                    "style": { "fontSize": 26, "fontFamily": "Inter, sans-serif", "textAlign": "center", "color": "#888888" }
                },
                {
                    "id": "message",
                    "type": "text",
                    "x": 200, "y": 1780, "width": 680, "height": 100,
                    "content": "Nous avons hâte de célébrer ce jour unique à vos côtés.",
                    "style": { "fontSize": 24, "fontFamily": "'Cormorant Garamond', serif", "textAlign": "center", "color": "#A0A0A0", "fontStyle": "italic" }
                }
            ]
        }
    }

    manifest_json = json.dumps({
        "id": t_data["id"],
        "name": t_data["name"],
        "required_plan": t_data["required_plan"],
        "default_config": t_data["default_config"]
    })

    existing = db.query(CardTemplate).filter(CardTemplate.id == t_id).first()
    if existing:
        existing.manifest_json = manifest_json
    else:
        new_t = CardTemplate(
            id=t_id,
            name=t_data["name"],
            description=t_data["description"],
            required_plan=t_data["required_plan"],
            manifest_json=manifest_json,
            thumbnail_url=t_data["thumbnail_url"]
        )
        db.add(new_t)
    
    db.commit()
    db.close()
    print(f"Template {t_id} synchronisé.")

if __name__ == "__main__":
    seed_ultimate_minimal()
