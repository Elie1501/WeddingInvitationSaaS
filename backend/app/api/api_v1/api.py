from fastapi import APIRouter
from app.api.api_v1.endpoints import auth
from app.api.api_v1.endpoints import guests
from app.api.api_v1.endpoints import table
from app.api.api_v1.endpoints import events

api_router = APIRouter()

# On lie le module auth sous le préfixe /auth
api_router.include_router(auth.router, prefix="/auth", tags=["login"])

api_router.include_router(events.router, prefix="/events", tags=["events"])

api_router.include_router(guests.router, prefix="/guests", tags=["guests"])

api_router.include_router(table.router, prefix="/tables", tags=["tables"])

