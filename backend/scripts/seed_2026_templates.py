"""
Seed les 4 templates 2026 : Éclipse, Lettre, Lumière, Sanctuaire.
Usage : python scripts/seed_2026_templates.py
"""
import os, sys, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.wedding import CardTemplate
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)

DEMO_SUB_EVENTS = [
    {"time": "14h00", "title": "Cérémonie civile",   "location": "Mairie de Provence"},
    {"time": "16h30", "title": "Cérémonie religieuse","location": "Chapelle Saint-Pierre", "description": "Accueil des invités à partir de 16h00."},
    {"time": "19h00", "title": "Vin d'honneur",       "location": "Terrasses du château"},
    {"time": "21h00", "title": "Dîner & soirée",      "location": "Grande salle du château"},
]

TEMPLATES = [
    {
        "id": "eclipse",
        "name": "Éclipse",
        "description": "Minimalisme éditorial 2026. Typographie Fraunces display en bas de casse, fond ivoire, accent terracotta. L'élégance par le vide et le rythme typographique.",
        "category": "minimal",
        "required_plan": "premium",
        "thumbnail_url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=400",
        "manifest": {
            "name": "Éclipse",
            "layout": "eclipse",
            "sections": ["hero"],
            "theme": {
                "background": "#F5F0E8",
                "accent": "#C0603A",
                "text": "#3D3730",
                "namesColor": "#1A1512",
                "countdownColor": "#C0603A",
                "sectionTitleColor": "#C0603A",
                "fontFamily": "Fraunces",
            },
            "content": {
                "names": "",
                "date_display": "",
                "address": "",
                "footer_text": "Fait avec amour · 2026",
            },
            "sub_events": DEMO_SUB_EVENTS,
            "show_countdown": True,
            "show_splash": False,
        },
    },
    {
        "id": "lettre",
        "name": "Lettre",
        "description": "Romantique haut de gamme, inspiration faire-part gravé. Script élégant Pinyon + Cormorant Garamond, grain papier CSS, filets fins, monogramme discret, accent or doux.",
        "category": "classic",
        "required_plan": "premium",
        "thumbnail_url": "https://images.unsplash.com/photo-1606216794079-73d0b3eb5d8c?w=400",
        "manifest": {
            "name": "Lettre",
            "layout": "lettre",
            "sections": ["hero"],
            "theme": {
                "background": "#FAF5EC",
                "accent": "#B89850",
                "text": "#3D2E1E",
                "namesColor": "#4A3220",
                "countdownColor": "#B89850",
                "sectionTitleColor": "#B89850",
                "fontFamily": "Cormorant Garamond",
            },
            "content": {
                "names": "",
                "date_display": "",
                "address": "",
                "footer_text": "Fait avec amour · 2026",
            },
            "sub_events": DEMO_SUB_EVENTS,
            "show_countdown": True,
            "show_splash": False,
        },
    },
    {
        "id": "lumiere",
        "name": "Lumière",
        "description": "Spiritualité contemporaine, clair et aéré. Halo lumineux CSS, verset optionnel, serif humaniste Newsreader, accent sauge doux pour couples croyants modernes.",
        "category": "spiritual",
        "required_plan": "premium",
        "thumbnail_url": "https://images.unsplash.com/photo-1534067783941-51c9c23ecefd?w=400",
        "manifest": {
            "name": "Lumière",
            "layout": "lumiere",
            "sections": ["hero"],
            "theme": {
                "background": "#FDFCFA",
                "accent": "#A8B89C",
                "text": "#3A4050",
                "namesColor": "#1C2028",
                "countdownColor": "#A8B89C",
                "sectionTitleColor": "#A8B89C",
                "fontFamily": "Newsreader",
            },
            "content": {
                "names": "",
                "date_display": "",
                "address": "",
                "verse": "« L'amour est patient, il est plein de bonté. » — 1 Co 13,4",
                "footer_text": "Fait avec amour · 2026",
            },
            "sub_events": DEMO_SUB_EVENTS,
            "show_countdown": True,
            "show_splash": False,
        },
    },
    {
        "id": "sanctuaire",
        "name": "Sanctuaire",
        "description": "Élégance sacrée et solennelle. Symbole spirituel configurable (croix / étoile / croissant), verset, EB Garamond + Spectral, or liturgique sobre. Intemporel.",
        "category": "spiritual",
        "required_plan": "premium",
        "thumbnail_url": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=400",
        "manifest": {
            "name": "Sanctuaire",
            "layout": "sanctuaire",
            "sections": ["hero"],
            "theme": {
                "background": "#F4EEE0",
                "accent": "#B8963C",
                "text": "#2C2010",
                "namesColor": "#1A1208",
                "countdownColor": "#B8963C",
                "sectionTitleColor": "#B8963C",
                "fontFamily": "EB Garamond",
            },
            "content": {
                "names": "",
                "date_display": "",
                "address": "",
                "verse": "« Ce que Dieu a uni, que l'homme ne le sépare pas. » — Mc 10,9",
                "symbol": "cross",
                "footer_text": "Fait avec amour · 2026",
            },
            "sub_events": DEMO_SUB_EVENTS,
            "show_countdown": True,
            "show_splash": False,
        },
    },
]


def seed():
    db = Session()
    try:
        for t in TEMPLATES:
            existing = db.query(CardTemplate).filter(CardTemplate.id == t["id"]).first()
            manifest_str = json.dumps(t["manifest"], ensure_ascii=False)
            if existing:
                existing.name          = t["name"]
                existing.description   = t["description"]
                existing.category      = t["category"]
                existing.required_plan = t["required_plan"]
                existing.thumbnail_url = t["thumbnail_url"]
                existing.manifest_json = manifest_str
                existing.is_active     = True
                print(f"  ✔ mis à jour : {t['id']}")
            else:
                db.add(CardTemplate(
                    id            = t["id"],
                    name          = t["name"],
                    description   = t["description"],
                    category      = t["category"],
                    required_plan = t["required_plan"],
                    thumbnail_url = t["thumbnail_url"],
                    manifest_json = manifest_str,
                    is_active     = True,
                ))
                print(f"  ✔ créé     : {t['id']}")
        db.commit()
        print("\nDone — 4 templates 2026 en base.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
