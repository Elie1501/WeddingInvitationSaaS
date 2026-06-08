import json
import os
import sys

# Ajouter le chemin du projet pour importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.wedding import CardTemplate, Card

def seed_art_templates():
    db = SessionLocal()
    
    # On n'efface plus tout pour éviter les IntegrityError avec les cartes existantes
    print("Mise à jour de la bibliothèque de templates...")
    
    templates = [
        {
            "id": "premium-frame",
            "name": "Cadre Premium",
            "description": "Un liseré doré subtil encadrant un design minimaliste et luxueux.",
            "required_plan": "premium",
            "thumbnail_url": "https://images.unsplash.com/photo-1465495910483-0d674577873d?w=400",
            "default_config": {
                "canvas": { 
                    "width": 1080, "height": 1920, 
                    "background_color": "#ffffff"
                },
                "has_cover_page": True,
                "elements": [
                    {
                        "id": "gold-frame",
                        "type": "shape",
                        "x": 60, "y": 60, "width": 960, "height": 1800,
                        "style": { "border": "3px solid #d4af37", "backgroundColor": "transparent" }
                    },
                    {
                        "id": "intro-text",
                        "type": "text",
                        "x": 140, "y": 250, "width": 800, "height": 100,
                        "content": "ONT L'HONNEUR DE VOUS CONVIER AU MARIAGE DE",
                        "style": { "fontSize": 20, "fontFamily": "Montserrat, sans-serif", "fontWeight": "500", "textAlign": "center", "color": "#888888", "letterSpacing": "6px", "lineHeight": "2" }
                    },
                    {
                        "id": "names-text",
                        "type": "text",
                        "x": 40, "y": 450, "width": 1000, "height": 200,
                        "content": "{groom_name}\n&\n{bride_name}",
                        "style": { "fontSize": 90, "fontFamily": "'Great Vibes', cursive", "fontWeight": "400", "textAlign": "center", "color": "#d4af37", "lineHeight": "1.2" }
                    },
                    {
                        "id": "center-image",
                        "type": "image",
                        "x": 240, "y": 800, "width": 600, "height": 750,
                        "content": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1080",
                        "style": { "objectFit": "cover", "filter": "grayscale(20%)" }
                    },
                    {
                        "id": "date-text",
                        "type": "text",
                        "x": 140, "y": 1650, "width": 800, "height": 100,
                        "content": "{date}\n{location}",
                        "style": { "fontSize": 26, "fontFamily": "'Cormorant Garamond', serif", "fontWeight": "600", "textAlign": "center", "color": "#333333", "letterSpacing": "2px", "lineHeight": "1.5" }
                    }
                ]
            }
        }
    ]

    for t_data in templates:
        manifest_json = json.dumps({
            "id": t_data["id"],
            "name": t_data["name"],
            "required_plan": t_data["required_plan"],
            "default_config": t_data["default_config"]
        })
        
        existing = db.query(CardTemplate).filter(CardTemplate.id == t_data["id"]).first()
        if existing:
            existing.name = t_data["name"]
            existing.description = t_data["description"]
            existing.required_plan = t_data["required_plan"]
            existing.manifest_json = manifest_json
            existing.thumbnail_url = t_data["thumbnail_url"]
            print(f"Template {t_data['id']} mis à jour.")
        else:
            new_t = CardTemplate(
                id=t_data["id"],
                name=t_data["name"],
                description=t_data["description"],
                required_plan=t_data["required_plan"],
                manifest_json=manifest_json,
                thumbnail_url=t_data["thumbnail_url"],
                is_active=True
            )
            db.add(new_t)
            print(f"Template {t_data['id']} créé.")
    
    db.commit()
    db.close()
    print("Mise à jour terminée avec succès !")

if __name__ == "__main__":
    seed_art_templates()