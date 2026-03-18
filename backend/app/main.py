from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine, Base
from app.api.api_v1.api import api_router # Import du routeur global
from app.models import wedding # Force le chargement des modèles pour SQLAlchemy

# Création des tables au démarrage (pour le dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Carte de Mariage",
    description="Backend pour la plateforme de gestion de mariages numériques",
    version="1.0.0"
)

# Configuration CORS
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONNEXION DES ROUTES
app.include_router(api_router)

@app.get("/")
async def health_check():
    return {"status": "online", "message": "API opérationnelle"}