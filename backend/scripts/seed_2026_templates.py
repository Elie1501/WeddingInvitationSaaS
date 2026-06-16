"""
Seed les templates 2026 : Éclipse, Amour.
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
        "id": "amour",
        "name": "Amour",
        "description": "Romantique et tendre. Cœur tracé qui bat, cœurs flottants, halo rosé, script Dancing Script et serif Cormorant. Doux et animé.",
        "category": "romantic",
        "required_plan": "free",
        "thumbnail_url": "https://images.unsplash.com/photo-1518568814500-bf0f8d125f46?w=400",
        "manifest": {
            "name": "Amour",
            "layout": "amour",
            "sections": ["hero"],
            "theme": {
                "background": "#FDF1F0",
                "accent": "#D6677A",
                "text": "#4A2E33",
                "namesColor": "#6B2737",
                "countdownColor": "#D6677A",
                "sectionTitleColor": "#D6677A",
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
