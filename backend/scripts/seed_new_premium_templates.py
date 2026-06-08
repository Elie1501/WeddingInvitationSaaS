import json, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal
from app.models.wedding import CardTemplate

TEMPLATES = [
    {
        "id": "cinema",
        "name": "Cinématique — Pellicule 35mm",
        "description": "Grain de film animé, révélation lettre par lettre, barres letterbox. L'esthétique la plus premium du cinéma classique.",
        "thumbnail_url": "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400&q=80",
        "manifest": {
            "layout": "cinema",
            "sections": ["cinema-full", "program", "footer"],
            "theme": {
                "background": "#080808",
                "accent": "#D4853A",
                "text": "#F0EAE0",
                "fontFamily": "Bebas Neue"
            },
            "content": {
                "names": "Emma & Lucas",
                "date_display": "15 juin 2026",
                "intro_text": "Deux âmes que le destin avait prédestinées. Une rencontre, une histoire, une vie entière à écrire ensemble.",
                "image_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200"
            }
        }
    },
    {
        "id": "celestial",
        "name": "Céleste — Nuit Étoilée",
        "description": "Particules d'étoiles animées, constellations progressives, parallaxe au scroll. Le plus spectaculaire.",
        "thumbnail_url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=400&q=80",
        "manifest": {
            "layout": "celestial",
            "sections": ["celestial-full", "program", "footer"],
            "theme": {
                "background": "#05050f",
                "accent": "#F0D080",
                "text": "#E8E0FF",
                "fontFamily": "Cinzel"
            },
            "content": {
                "names": "Emma & Lucas",
                "date_display": "15 juin 2026",
                "intro_text": "\"Nos âmes se sont reconnues parmi des milliers d'étoiles.\""
            }
        }
    },
    {
        "id": "wabi-sabi",
        "name": "Wabi-Sabi — Jardin Japonais",
        "description": "Traits d'encre qui se dessinent en SVG, pétales tombants, papier ivoire texturé. Élégance zen.",
        "thumbnail_url": "https://images.unsplash.com/photo-1490750967868-88df5691cc84?w=400&q=80",
        "manifest": {
            "layout": "wabi-sabi",
            "sections": ["wabi-sabi-full", "program", "footer"],
            "theme": {
                "background": "#F7F4EE",
                "accent": "#C4718A",
                "text": "#2C2416",
                "fontFamily": "Noto Serif JP"
            },
            "content": {
                "names": "Emma & Lucas",
                "date_display": "15 juin 2026",
                "intro_text": "\"L'imperfection est la plus belle des perfections.\"",
                "image_url": "https://images.unsplash.com/photo-1490750967868-88df5691cc84?w=1200"
            }
        }
    },
    {
        "id": "gatsby",
        "name": "Art Déco — Grande Gatsby",
        "description": "Lignes géométriques qui se construisent au chargement, or scintillant, symétrie absolue années 20.",
        "thumbnail_url": "https://images.unsplash.com/photo-1519741497674-611481863552?w=400&q=80",
        "manifest": {
            "layout": "gatsby",
            "sections": ["gatsby-full", "program", "footer"],
            "theme": {
                "background": "#100e08",
                "accent": "#D4A853",
                "text": "#F5E6C8",
                "fontFamily": "Cinzel Decorative"
            },
            "content": {
                "names": "Emma & Lucas",
                "date_display": "15 JUIN 2026",
                "intro_text": "Vous convier à la célébration somptueuse de notre union dans la grande tradition des soirées d'exception.",
                "dress_code": "Black Tie",
                "image_url": "https://images.unsplash.com/photo-1519741497674-611481863552?w=1200"
            }
        }
    },
    {
        "id": "botanical",
        "name": "Botanical — Herbarium Nuptiale",
        "description": "Illustrations botaniques SVG qui s'animent au chargement, mise en page organique, scroll révélation.",
        "thumbnail_url": "https://images.unsplash.com/photo-1508610048659-a06b669e3321?w=400&q=80",
        "manifest": {
            "layout": "botanical",
            "sections": ["botanical-full", "program", "footer"],
            "theme": {
                "background": "#FAF8F2",
                "accent": "#C4714A",
                "text": "#2D2318",
                "fontFamily": "Playfair Display"
            },
            "content": {
                "names": "Emma & Lucas",
                "date_display": "15 juin 2026",
                "intro_text": "\"La nature est le plus beau des décors pour une histoire d'amour.\"",
                "dress_code": "Couleurs florales",
                "image_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200",
                "image_url_2": "https://images.unsplash.com/photo-1495107334309-fcf20504a5ab?w=800"
            }
        }
    },
    {
        "id": "editorial",
        "name": "Éditorial Brutaliste — Avant-Garde",
        "description": "Typographie massive, marquee luxueux, snap mécanique, grille révélée. Le plus inattendu pour un mariage.",
        "thumbnail_url": "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?w=400&q=80",
        "manifest": {
            "layout": "editorial",
            "sections": ["editorial-full", "program", "footer"],
            "theme": {
                "background": "#FFFFFF",
                "accent": "#E63946",
                "text": "#0A0A0A",
                "fontFamily": "Space Grotesk"
            },
            "content": {
                "names": "Emma & Lucas",
                "date_display": "15 JUIN 2026",
                "intro_text": "Une invitation à témoigner de l'union la plus importante de l'année. Une soirée hors du temps.",
                "image_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200"
            }
        }
    },
    {
        "id": "velvet-noir",
        "name": "Velvet Noir — Luxe Nocturne",
        "description": "Rideaux qui s'ouvrent, flammes CSS, particules lumineuses ascendantes, texture velours. Le plus sensuel.",
        "thumbnail_url": "https://images.unsplash.com/photo-1519741497674-611481863552?w=400&q=80",
        "manifest": {
            "layout": "velvet-noir",
            "sections": ["velvet-noir-full", "program", "footer"],
            "theme": {
                "background": "#1a0610",
                "accent": "#E8B4A0",
                "text": "#F5E8E0",
                "fontFamily": "Cormorant Garamond"
            },
            "content": {
                "names": "Emma & Lucas",
                "date_display": "15 juin 2026",
                "intro_text": "\"Laissez-vous envelopper par la douceur d'une nuit de velours, où l'amour brille comme mille bougies.\"",
                "dress_code": "Tenue de soirée",
                "image_url": "https://images.unsplash.com/photo-1519741497674-611481863552?w=1200"
            }
        }
    },
]

def seed():
    db = SessionLocal()
    for t in TEMPLATES:
        manifest_json = json.dumps({
            "name": t["name"],
            "description": t["description"],
            "default_config": t["manifest"]
        })
        existing = db.query(CardTemplate).filter(CardTemplate.id == t["id"]).first()
        if existing:
            existing.name = t["name"]
            existing.description = t["description"]
            existing.thumbnail_url = t["thumbnail_url"]
            existing.manifest_json = manifest_json
            print(f"Mis à jour: {t['id']}")
        else:
            db.add(CardTemplate(
                id=t["id"],
                name=t["name"],
                description=t["description"],
                thumbnail_url=t["thumbnail_url"],
                manifest_json=manifest_json,
                required_plan="premium",
                is_active=True
            ))
            print(f"Créé: {t['id']}")
    db.commit()
    db.close()
    print("✓ 7 nouveaux templates premium ajoutés.")

if __name__ == "__main__":
    seed()
