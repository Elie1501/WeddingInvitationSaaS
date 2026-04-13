from fastapi import APIRouter
from app.api.api_v1.endpoints import auth
from app.api.api_v1.endpoints import guests
from app.api.api_v1.endpoints import table
from app.api.api_v1.endpoints import events
from app.api.api_v1.endpoints import cards
from app.api.api_v1.endpoints import templates
from app.api.api_v1.endpoints import users

api_router = APIRouter()

# On lie le module auth sous le préfixe /auth
api_router.include_router(auth.router, prefix="/auth", tags=["login"])

api_router.include_router(users.router, prefix="/users", tags=["users"])

api_router.include_router(events.router, prefix="/events", tags=["events"])

api_router.include_router(guests.router, prefix="/guests", tags=["guests"])

api_router.include_router(table.router, prefix="/tables", tags=["tables"])

api_router.include_router(cards.router, prefix="/cards", tags=["cards"])

api_router.include_router(templates.router, prefix="/templates", tags=["templates"])

