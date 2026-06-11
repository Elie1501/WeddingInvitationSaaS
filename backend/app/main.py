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

# ── Config des templates valides : (catégorie, thumbnail HD, nom d'affichage, plan requis)
# Tout template listé ici est activé automatiquement au démarrage.
TEMPLATE_CATALOG = {
    # ── Classic (accès gratuit) ──────────────────────────────────────────────
    "noir-eternel":      ("minimal", "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800&q=80", "Noir Éternel",                "classic"),
    "riviera-blanche":   ("minimal", "https://images.unsplash.com/photo-1529636444744-adffc9135a5e?w=800&q=80", "Riviera Blanche",             "classic"),
    "couture":           ("minimal", "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&q=80", "Maison de Haute Couture",     "classic"),
    "cinema":            ("classic", "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800&q=80", "Cinématique — Pellicule 35mm","classic"),
    "gatsby":            ("classic", "https://images.unsplash.com/photo-1467810563316-b5476525c0f9?w=800&q=80", "Art Déco — Grande Gatsby",    "classic"),
    "jardin-celeste":    ("boho",    "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=800&q=80", "Jardin Céleste",              "classic"),
    "japonais":          ("boho",    "https://images.unsplash.com/photo-1528360983277-13d401cdc186?w=800&q=80", "Jardin Japonais",             "classic"),
    "editorial":         ("art",     "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=800&q=80", "Éditorial Brutaliste",        "classic"),
    # ── Premium ─────────────────────────────────────────────────────────────
    "velvet-noir":       ("minimal", "https://images.unsplash.com/photo-1519741497674-611481863552?w=800&q=80", "Velvet Noir",                 "premium"),
    "ora":               ("classic", "https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=800&q=80", "Éclat Doré",                  "premium"),
    "empire-abstrait":   ("classic", "https://images.unsplash.com/photo-1600585154526-990dced4db0d?w=800&q=80", "Empire Abstrait",             "premium"),
    "brutaliste":        ("art",     "https://images.unsplash.com/photo-1486325212027-8081e485255e?w=800&q=80", "Architecture Brutaliste",     "premium"),
    "film":              ("art",     "https://images.unsplash.com/photo-1476357471311-43c0db9fb2b4?w=800&q=80", "Sépia & Film Argentique",     "premium"),
    "celestial":         ("art",     "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?w=800&q=80", "Céleste — Nuit Étoilée",      "premium"),
    "riviera":           ("boho",    "https://images.unsplash.com/photo-1537633552985-df8429e8048b?w=800&q=80", "Riviera Anni 70",             "premium"),
    "wabi-sabi":         ("boho",    "https://images.unsplash.com/photo-1523301343968-6a6ebf63c672?w=800&q=80", "Wabi-Sabi — Jardin Japonais", "premium"),
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

        # Créer ou mettre à jour tous les templates du catalogue
        for tpl_id, (category, thumbnail, name, plan) in TEMPLATE_CATALOG.items():
            tpl = db.query(CardTemplate).filter(CardTemplate.id == tpl_id).first()
            if tpl:
                tpl.is_active     = True
                tpl.category      = category
                tpl.thumbnail_url = thumbnail
                tpl.name          = name
                tpl.required_plan = plan
            else:
                db.add(CardTemplate(
                    id=tpl_id,
                    name=name,
                    category=category,
                    thumbnail_url=thumbnail,
                    is_active=True,
                    manifest_json="{}",
                    required_plan=plan,
                ))

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
