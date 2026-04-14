from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import os
from app.db.session import engine, Base, SessionLocal
from app.api.api_v1.api import api_router # Import du routeur global
from app.models.wedding import CardTemplate, User # Force le chargement des modèles pour SQLAlchemy
from app.core import security

# Création des tables au démarrage (pour le dev)
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    # 1. Seed Templates
    templates = [
        {
            "id": "modern-chic",
            "name": "Modern Chic",
            "description": "Design minimaliste et typographie audacieuse.",
            "thumbnail_url": "https://placehold.co/400x300?text=Modern+Chic",
            "required_plan": "free",
            "default_config": {
                "colors": {"primary": "#000000", "accent": "#6366f1", "background": "#ffffff", "text": "#111827"},
                "typography": {"headings": "Inter", "body": "Inter"},
                "sections": [{"type": "banner", "id": "b1"}, {"type": "text", "id": "t1"}, {"type": "details", "id": "d1"}]
            }
        },
        {
            "id": "classic-elegance",
            "name": "Élégance Classique",
            "description": "Traditionnel et raffiné, tons crème.",
            "thumbnail_url": "https://placehold.co/400x300?text=Classic+Elegance",
            "required_plan": "classic",
            "default_config": {
                "colors": {"primary": "#451a03", "accent": "#92400e", "background": "#fef3c7", "text": "#451a03"},
                "typography": {"headings": "Playfair Display", "body": "Playfair Display"},
                "sections": [{"type": "banner", "id": "b1"}, {"type": "text", "id": "t1"}, {"type": "details", "id": "d1"}]
            }
        },
        {
            "id": "royal-gold",
            "name": "Royal Gold",
            "description": "Luxe absolu, noir et or avec ornements majestueux.",
            "thumbnail_url": "https://placehold.co/400x300?text=Royal+Gold",
            "required_plan": "premium",
            "default_config": {
                "colors": {"primary": "#d4af37", "accent": "#d4af37", "background": "#0c0a09", "text": "#f5f5f4"},
                "typography": {"headings": "Great Vibes", "body": "Cormorant Garamond"},
                "sections": [{"type": "banner", "id": "b1"}, {"type": "text", "id": "t1"}, {"type": "details", "id": "d1"}]
            }
        },
        {
            "id": "bohemian-dream",
            "name": "Bohemian Dream",
            "description": "Esprit champêtre, tons terreux et fleurs séchées.",
            "thumbnail_url": "https://placehold.co/400x300?text=Bohemian+Dream",
            "required_plan": "classic",
            "default_config": {
                "colors": {"primary": "#c46647", "accent": "#c46647", "background": "#fdf8f3", "text": "#4a3728"},
                "typography": {"headings": "Playfair Display", "body": "Montserrat"},
                "sections": [{"type": "banner", "id": "b1"}, {"type": "text", "id": "t1"}, {"type": "details", "id": "d1"}]
            }
        },
        {
            "id": "midnight-glamour",
            "name": "Midnight Glamour",
            "description": "Ambiance nocturne, dégradés profonds et chic urbain.",
            "thumbnail_url": "https://placehold.co/400x300?text=Midnight+Glamour",
            "required_plan": "premium",
            "default_config": {
                "colors": {"primary": "#ffffff", "accent": "#818cf8", "background": "#020617", "text": "#f8fafc"},
                "typography": {"headings": "Cormorant Garamond", "body": "Cormorant Garamond"},
                "sections": [{"type": "banner", "id": "b1"}, {"type": "text", "id": "t1"}, {"type": "details", "id": "d1"}]
            }
        }
    ]
    
    for t in templates:
        existing = db.query(CardTemplate).filter(CardTemplate.id == t["id"]).first()
        if not existing:
            new_tpl = CardTemplate(
                id=t["id"],
                name=t["name"],
                description=t["description"],
                thumbnail_url=t["thumbnail_url"],
                required_plan=t.get("required_plan", "classic"),
                manifest_json=json.dumps(t)
            )
            db.add(new_tpl)

    # 2. Seed Test Users
    users_to_create = [
        {"email": "test@test.com", "password": "password123", "plan": "premium"},
        {"email": "admin@wedding.com", "password": "password123", "plan": "premium"},
        {"email": "marie@classic.com", "password": "password123", "plan": "classic"},
        {"email": "thomas@premium.com", "password": "password123", "plan": "premium"},
    ]
    for u_data in users_to_create:
        existing_user = db.query(User).filter(User.email == u_data["email"]).first()
        if not existing_user:
            new_user = User(
                email=u_data["email"],
                hashed_password=security.get_password_hash(u_data["password"]),
                plan=u_data["plan"]
            )
            db.add(new_user)
            print(f"Utilisateur de test créé : {u_data['email']}")

    db.commit()
    db.close()

seed_data()

app = FastAPI(
    title="API Carte de Mariage",
    description="Backend pour la plateforme de gestion de mariages numériques",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONNEXION DES ROUTES
app.include_router(api_router)

# Montage des fichiers statiques pour les uploads
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
async def health_check():
    return {"status": "online", "message": "API opérationnelle"}
