import json
import os
import sys

# Ajouter le chemin du projet pour importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.wedding import CardTemplate, Card

def seed_art_templates():
    db = SessionLocal()
    
    # Nettoyage sécurisé
    print("Détachement des cartes existantes...")
    db.query(Card).update({Card.template_id: None})
    db.commit()

    print("Nettoyage de la bibliothèque de templates...")
    db.query(CardTemplate).delete()
    db.commit()
    
    templates = [
        {
            "id": "elegant-fullscreen",
            "name": "Élégance Absolue (Plein Écran)",
            "description": "Design premium avec image plein écran, overlay sombre et typographie luxe.",
            "required_plan": "classic",
            "thumbnail_url": "https://images.unsplash.com/photo-1519741497674-611481863552?w=400",
            "default_config": {
                "canvas": { 
                    "width": 1080, "height": 1920, 
                    "background_color": "#000000"
                },
                "has_cover_page": True,
                "elements": [
                    {
                        "id": "bg-image",
                        "type": "image",
                        "x": 0, "y": 0, "width": 1080, "height": 1920,
                        "content": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=1080",
                        "style": { "objectFit": "cover" }
                    },
                    {
                        "id": "overlay",
                        "type": "shape",
                        "x": 0, "y": 0, "width": 1080, "height": 1920,
                        "style": { "backgroundColor": "#000000", "opacity": "0.4" }
                    },
                    {
                        "id": "intro-text",
                        "type": "text",
                        "x": 140, "y": 600, "width": 800, "height": 100,
                        "content": "NOUS NOUS MARIONS",
                        "style": { "fontSize": 24, "fontFamily": "Inter, sans-serif", "fontWeight": "300", "textAlign": "center", "color": "#ffffff", "letterSpacing": "8px", "textTransform": "uppercase" }
                    },
                    {
                        "id": "names-text",
                        "type": "text",
                        "x": 40, "y": 750, "width": 1000, "height": 200,
                        "content": "{groom_name} & {bride_name}",
                        "style": { "fontSize": 110, "fontFamily": "'Playfair Display', serif", "fontWeight": "400", "textAlign": "center", "color": "#ffffff", "fontStyle": "italic" }
                    },
                    {
                        "id": "separator",
                        "type": "shape",
                        "x": 490, "y": 1050, "width": 100, "height": 2,
                        "style": { "backgroundColor": "#ffffff" }
                    },
                    {
                        "id": "details-text",
                        "type": "text",
                        "x": 140, "y": 1150, "width": 800, "height": 100,
                        "content": "{date}\n{location}",
                        "style": { "fontSize": 28, "fontFamily": "Montserrat, sans-serif", "fontWeight": "400", "textAlign": "center", "color": "#ffffff", "letterSpacing": "4px", "lineHeight": "2" }
                    }
                ]
            }
        },
        {
            "id": "luxe-arch",
            "name": "Arche Romantique",
            "description": "Composition épurée avec une image découpée en arche élégante sur fond clair.",
            "required_plan": "classic",
            "thumbnail_url": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=400",
            "default_config": {
                "canvas": { 
                    "width": 1080, "height": 1920, 
                    "background_color": "#fdfcf8"
                },
                "has_cover_page": True,
                "elements": [
                    {
                        "id": "arch-image",
                        "type": "image",
                        "x": 140, "y": 200, "width": 800, "height": 1100,
                        "content": "https://images.unsplash.com/photo-1522673607200-16488352475b?w=1080",
                        "style": { "objectFit": "cover", "borderRadius": "400px 400px 0 0" }
                    },
                    {
                        "id": "names-text",
                        "type": "text",
                        "x": 40, "y": 1450, "width": 1000, "height": 150,
                        "content": "{groom_name} & {bride_name}",
                        "style": { "fontSize": 90, "fontFamily": "'Cormorant Garamond', serif", "fontWeight": "400", "textAlign": "center", "color": "#2c2c2c" }
                    },
                    {
                        "id": "details-text",
                        "type": "text",
                        "x": 140, "y": 1650, "width": 800, "height": 100,
                        "content": "{date}  —  {location}",
                        "style": { "fontSize": 24, "fontFamily": "Inter, sans-serif", "fontWeight": "400", "textAlign": "center", "color": "#666666", "letterSpacing": "4px", "textTransform": "uppercase" }
                    }
                ]
            }
        },
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
        new_t = CardTemplate(
            id=t_data["id"],
            name=t_data["name"],
            description=t_data["description"],
            required_plan=t_data["required_plan"],
            manifest_json=manifest_json,
            thumbnail_url=t_data["thumbnail_url"]
        )
        db.add(new_t)
        print(f"Template {t_data['id']} créé.")
    
    db.commit()
    db.close()
    print("Mise à jour terminée avec succès !")

if __name__ == "__main__":
    seed_art_templates()