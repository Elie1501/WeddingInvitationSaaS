import json
import os
import sys

# Ajouter le chemin du projet pour importer les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.wedding import CardTemplate

def seed_premium_art_templates():
    db = SessionLocal()
    
    new_templates = [
        {
            "id": "cosmos",
            "name": "Cosmos & Céleste",
            "description": "Une esthétique observatoire astronomique romantique. Deux âmes qui se retrouvent sous les étoiles.",
            "thumbnail_url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=400&q=80",
            "manifest": {
                "layout": "cosmos",
                "sections": ["cosmos-full", "program", "rsvp", "footer"],
                "theme": {
                    "background": "#060814",
                    "accent": "#FFD700",
                    "text": "#F0F4FF",
                    "fontFamily": "Cormorant Garamond"
                },
                "content": {
                    "names": "Stella & Orion",
                    "image_url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=1200"
                }
            }
        },
        {
            "id": "couture",
            "name": "Maison de Haute Couture",
            "description": "L'élégance exclusive d'une maison de couture parisienne. Pureté, luxe et silence feutré.",
            "thumbnail_url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=400&q=80",
            "manifest": {
                "layout": "couture",
                "sections": ["couture-full", "program", "rsvp", "footer"],
                "theme": {
                    "background": "#FFFFFF",
                    "accent": "#000000",
                    "text": "#000000",
                    "fontFamily": "Bodoni Moda"
                },
                "content": {
                    "names": "COUTURE & MODA",
                    "image_url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=1200"
                }
            }
        }
    ]

    for t_data in new_templates:
        manifest_to_save = {
            "name": t_data["name"],
            "description": t_data["description"],
            "default_config": t_data["manifest"]
        }
        
        existing = db.query(CardTemplate).filter(CardTemplate.id == t_data["id"]).first()
        if existing:
            existing.name = t_data["name"]
            existing.description = t_data["description"]
            existing.thumbnail_url = t_data["thumbnail_url"]
            existing.manifest_json = json.dumps(manifest_to_save)
        else:
            new_t = CardTemplate(
                id=t_data["id"],
                name=t_data["name"],
                description=t_data["description"],
                thumbnail_url=t_data["thumbnail_url"],
                manifest_json=json.dumps(manifest_to_save),
                required_plan="premium",
                is_active=True
            )
            db.add(new_t)
        print(f"Template {t_data['id']} synchronisé.")
    
    db.commit()
    db.close()
    print("Mise à jour des templates premium terminée !")

if __name__ == "__main__":
    seed_premium_art_templates()
