from fastapi import APIRouter
from app.api.api_v1.endpoints import auth

api_router = APIRouter()

# On lie le module auth sous le préfixe /auth
api_router.include_router(auth.router, prefix="/auth", tags=["login"])