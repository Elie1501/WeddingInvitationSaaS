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
            "description": "Un design épuré et moderne avec une typographie serif élégante.",
            "thumbnail_url": "https://placehold.co/400x300?text=Modern+Chic",
            "required_plan": "classic",
            "default_config": {
                "colors": {"primary": "#1a1a1a", "accent": "#d4af37", "text": "#333333"},
                "typography": {"headings": "serif", "body": "sans-serif"},
                "sections": [
                    {"type": "banner", "id": "banner-1"},
                    {"type": "text", "id": "intro-1"},
                    {"type": "details", "id": "details-1"}
                ]
            }
        },
        {
            "id": "classic-elegance",
            "name": "Élégance Classique",
            "description": "Un design traditionnel avec des tons crème et une typographie cursive.",
            "thumbnail_url": "https://placehold.co/400x300?text=Classic+Elegance",
            "required_plan": "classic",
            "default_config": {
                "colors": {"primary": "#4a3b2b", "accent": "#c5a059", "text": "#5d4a37"},
                "typography": {"headings": "cursive", "body": "serif"},
                "sections": [
                    {"type": "banner", "id": "banner-classic"},
                    {"type": "text", "id": "intro-classic"},
                    {"type": "details", "id": "details-classic"}
                ]
            }
        },
        {
            "id": "romantic-garden",
            "name": "Jardin Romantique",
            "description": "Thème floral avec des tons pastels et une ambiance champêtre.",
            "thumbnail_url": "https://placehold.co/400x300?text=Romantic+Garden",
            "required_plan": "premium",
            "default_config": {
                "colors": {"primary": "#e8f5e9", "accent": "#81c784", "text": "#2e7d32"},
                "typography": {"headings": "cursive", "body": "serif"},
                "sections": [
                    {"type": "banner", "id": "banner-floral"},
                    {"type": "text", "id": "intro-floral"},
                    {"type": "details", "id": "details-floral"}
                ]
            }
        },
        {
            "id": "luxury-minimal",
            "name": "Luxe Minimaliste",
            "description": "Épure totale, typographie haute couture et contrastes forts.",
            "thumbnail_url": "https://placehold.co/400x300?text=Luxury+Minimal",
            "required_plan": "premium",
            "default_config": {
                "colors": {"primary": "#ffffff", "accent": "#000000", "text": "#1a1a1a"},
                "typography": {"headings": "serif", "body": "serif"},
                "sections": [
                    {"type": "banner", "id": "banner-lux"},
                    {"type": "text", "id": "intro-lux"},
                    {"type": "details", "id": "details-lux"}
                ]
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
