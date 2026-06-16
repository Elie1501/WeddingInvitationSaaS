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

# ── Config des templates valides : (catégorie, thumbnail HD, nom d'affichage)
# Tout template listé ici est activé automatiquement au démarrage.
# Aligné sur frontend/src/data/demoConfigs.js (l'id == clé de layout CardRenderer).
TEMPLATE_CATALOG = {
    "riviera-blanche":   ("minimal", "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=800&q=80", "Riviera Blanche"),
    "velvet-noir":       ("minimal", "https://images.unsplash.com/photo-1606800052052-a08af7148866?w=800&q=80", "Velvet Noir"),
    "gatsby":            ("classic", "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=800&q=80", "Art Déco"),
    "celestial":         ("art",     "https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?w=800&q=80", "Céleste"),
    "tel-aviv":          ("classic", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&q=80", "Tel Aviv"),
    "japonais":          ("boho",    "https://images.unsplash.com/photo-1522383225653-ed111181a951?w=800&q=80", "Japonais"),
    "riviera":           ("boho",    "https://images.unsplash.com/photo-1537633552985-df8429e8048b?w=800&q=80", "Riviera"),
    "cinema":            ("classic", "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800&q=80", "Cinéma"),
    "jardin-celeste":    ("boho",    "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80", "Jardin Céleste"),
    "empire-abstrait":   ("art",     "https://images.unsplash.com/photo-1518895949257-7621c3c786d7?w=800&q=80", "Empire Abstrait"),
    "ora":               ("minimal", "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&q=80", "Ora"),
    "film":              ("art",     "https://images.unsplash.com/photo-1476357471311-43c0db9fb2b4?w=800&q=80", "Pellicule"),
    "eclipse":           ("minimal", "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800&q=80", "Éclipse"),
    "amour":             ("minimal", "https://images.unsplash.com/photo-1494955870715-979ca4f13bf0?w=800&q=80", "Amour"),
}

def seed_data():
    from sqlalchemy import text
    db = SessionLocal()
    try:
        # Ajouter la colonne category si elle n'existe pas encore
        try:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE card_templates ADD COLUMN category VARCHAR DEFAULT 'minimal'"))
                conn.commit()
        except Exception:
            pass  # colonne déjà présente

        try:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE cards ADD COLUMN created_at TIMESTAMP DEFAULT NOW()"))
                conn.commit()
        except Exception:
            pass  # colonne déjà présente

        try:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT NOW()"))
                conn.commit()
        except Exception:
            pass  # colonne déjà présente

        # ── Auto-seed au démarrage (idempotent) ──────────────────────────
        # Garantit que comptes de démo + galerie de templates existent
        # même après une réinitialisation de la base de données.
        try:
            from scripts.seed_users import seed_users
            seed_users()
        except Exception as e:
            print(f"[seed] users: {e}")
        try:
            from scripts.seed_gallery import seed as seed_gallery
            seed_gallery()
        except Exception as e:
            print(f"[seed] gallery: {e}")

        # Activer + configurer tous les templates du catalogue
        for tpl_id, (category, thumbnail, name) in TEMPLATE_CATALOG.items():
            tpl = db.query(CardTemplate).filter(CardTemplate.id == tpl_id).first()
            if tpl:
                tpl.is_active  = True
                tpl.category   = category
                tpl.thumbnail_url = thumbnail

        # Désactiver les entrées orphelines (doublons, anciens IDs, sans composant Vue)
        db.query(CardTemplate).filter(
            ~CardTemplate.id.in_(list(TEMPLATE_CATALOG.keys()))
        ).update({CardTemplate.is_active: False}, synchronize_session=False)

        db.commit()
    finally:
        db.close()

seed_data()

app = FastAPI(title="API Mariage", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router)

if not os.path.exists("uploads"): os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def health_check(): return {"status": "online"}
