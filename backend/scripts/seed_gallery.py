"""
Seed la galerie publique (table card_templates) avec les 14 templates actuels.
Source de vérité alignée sur frontend/src/data/demoConfigs.js.
L'id de chaque template == clé de layout attendue par CardRenderer.vue.

Usage : python scripts/seed_gallery.py   (ou via docker compose exec)
"""
import os, sys, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import SessionLocal, engine, Base
from app.models.wedding import CardTemplate

Base.metadata.create_all(bind=engine)

THUMB = "https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&q=80&w=600"
FULL_SECTIONS = ["hero", "countdown", "program", "rsvp", "footer"]
HERO_ONLY = ["hero"]

# (id, name, premium?, category, sections, theme, thumbnail)
TEMPLATES = [
    ("riviera-blanche", "Riviera Blanche", False, "minimal", FULL_SECTIONS,
     {"background": "#FAFAF8", "accent": "#2E6E8E", "text": "#1C2B3A", "fontFamily": "Playfair Display"},
     "https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&q=80&w=600"),
    ("velvet-noir", "Velvet Noir", True, "minimal", FULL_SECTIONS,
     {"background": "#1a0610", "accent": "#E8B4A0", "text": "#F5E8E0", "fontFamily": "Cormorant Garamond"},
     "https://images.unsplash.com/photo-1606800052052-a08af7148866?auto=format&fit=crop&q=80&w=600"),
    ("gatsby", "Art Déco", True, "classic", FULL_SECTIONS,
     {"background": "#100e08", "accent": "#D4A853", "text": "#F5E6C8", "fontFamily": "Cinzel"},
     "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&q=80&w=600"),
    ("celestial", "Céleste", True, "art", FULL_SECTIONS,
     {"background": "#05050f", "accent": "#F0D080", "text": "#E8E0FF", "fontFamily": "Cormorant Garamond"},
     "https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?auto=format&fit=crop&q=80&w=600"),
    ("tel-aviv", "Tel Aviv", False, "classic", FULL_SECTIONS,
     {"background": "#FBF9F4", "accent": "#0038B8", "text": "#1A2238", "namesColor": "#16203A", "countdownColor": "#0038B8", "fontFamily": "Cormorant Garamond"},
     "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&q=80&w=600"),
    ("japonais", "Japonais", False, "boho", FULL_SECTIONS,
     {"background": "#F7EEE3", "accent": "#D14B3D", "text": "#2A1E18", "fontFamily": "Shippori Mincho"},
     "https://images.unsplash.com/photo-1522383225653-ed111181a951?auto=format&fit=crop&q=80&w=600"),
    ("riviera", "Riviera", False, "boho", FULL_SECTIONS,
     {"background": "#F0EBE3", "accent": "#7B9EA6", "text": "#2D3436", "fontFamily": "Playfair Display"},
     "https://images.unsplash.com/photo-1537633552985-df8429e8048b?auto=format&fit=crop&q=80&w=600"),
    ("cinema", "Cinéma", True, "classic", FULL_SECTIONS,
     {"background": "#080808", "accent": "#D4853A", "text": "#F0EAE0", "fontFamily": "Lato"},
     "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&q=80&w=600"),
    ("jardin-celeste", "Jardin Céleste", False, "boho", FULL_SECTIONS,
     {"background": "#0F2419", "accent": "#D9E86B", "text": "#F2EBE0", "fontFamily": "Cormorant Upright"},
     "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=600"),
    ("empire-abstrait", "Empire Abstrait", True, "art", FULL_SECTIONS,
     {"background": "#0E0C18", "accent": "#FF6B6B", "text": "#EDE9F5", "namesColor": "#FFFFFF", "countdownColor": "#FF6B6B", "fontFamily": "Space Grotesk"},
     "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?auto=format&fit=crop&q=80&w=600"),
    ("ora", "Ora", False, "minimal", FULL_SECTIONS,
     {"background": "#FFF9F3", "accent": "#D4956A", "text": "#2A1A0E", "fontFamily": "Cormorant Garamond"},
     "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&q=80&w=600"),
    ("film", "Pellicule", True, "art", FULL_SECTIONS,
     {"background": "#F2E9DB", "accent": "#C77F4E", "text": "#3A2E24", "fontFamily": "Cormorant Garamond"},
     "https://images.unsplash.com/photo-1476357471311-43c0db9fb2b4?auto=format&fit=crop&q=80&w=600"),
    ("eclipse", "Éclipse", True, "minimal", FULL_SECTIONS,
     {"background": "#1B1430", "accent": "#F0A85C", "text": "#E8DFF0", "namesColor": "#FBF3E8", "countdownColor": "#F0A85C", "sectionTitleColor": "#F0A85C", "fontFamily": "Fraunces"},
     "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&q=80&w=600"),
    ("amour", "Amour", False, "minimal", FULL_SECTIONS,
     {"background": "#FDF1F0", "accent": "#D6677A", "text": "#4A2E33", "namesColor": "#6B2737", "countdownColor": "#D6677A", "sectionTitleColor": "#D6677A", "fontFamily": "Cormorant Garamond"},
     "https://images.unsplash.com/photo-1494955870715-979ca4f13bf0?auto=format&fit=crop&q=80&w=600"),
]

DESCRIPTIONS = {
    "riviera-blanche": "Élégance côtière épurée, branche d'olivier dessinée, bleu Méditerranée.",
    "velvet-noir": "Velours sombre et raffiné, accents poudrés, ambiance soirée.",
    "gatsby": "Art Déco doré années folles, géométrie et faste.",
    "celestial": "Nuit étoilée, constellation tracée, or sur bleu nuit.",
    "tel-aviv": "Identité juive/israélienne : étoile de David, מַזָּל טוֹב, azur méditerranéen.",
    "japonais": "Soleil levant, Mont Fuji, pétales de sakura, tampon 寿.",
    "riviera": "Côte d'Azur seventies, photo et lettrage chic.",
    "cinema": "Carton-titre de cinéma, letterbox, grain de pellicule.",
    "jardin-celeste": "Jardin nocturne, ciel étoilé, lucioles et lune.",
    "empire-abstrait": "Aurora animée, typographie bold, modernité abstraite.",
    "ora": "Lumière chaude et minimale, sérif délicat.",
    "film": "Album photo argentique, polaroids, légende manuscrite.",
    "eclipse": "Minimalisme contemporain, sérif Fraunces, sobriété chic.",
    "amour": "Romantique et tendre, cœur animé, cœurs flottants, halo rosé.",
}


def seed():
    db = SessionLocal()
    try:
        keep_ids = []
        for tpl_id, name, premium, category, sections, theme, thumb in TEMPLATES:
            keep_ids.append(tpl_id)
            manifest = {
                "name": name,
                "layout": tpl_id,
                "sections": sections,
                "theme": theme,
                "content": {"footer_text": "Fait avec amour · 2026"},
                "show_countdown": True,
                "show_splash": False,
            }
            row = db.query(CardTemplate).filter(CardTemplate.id == tpl_id).first()
            if not row:
                row = CardTemplate(id=tpl_id)
                db.add(row)
            row.name = name
            row.description = DESCRIPTIONS.get(tpl_id, "")
            row.required_plan = "premium" if premium else "classic"
            row.manifest_json = json.dumps(manifest, ensure_ascii=False)
            row.thumbnail_url = thumb
            row.category = category
            row.is_active = True

        # Désactiver tout template hors liste (anciens / supprimés)
        db.query(CardTemplate).filter(~CardTemplate.id.in_(keep_ids)).update(
            {CardTemplate.is_active: False}, synchronize_session=False
        )
        db.commit()
        print(f"✅ {len(TEMPLATES)} templates seedés et activés.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
