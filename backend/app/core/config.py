import logging
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DATABASE_URL: str

    S3_BUCKET: str = "wedding-invitations-media"
    S3_REGION: str = "eu-west-3"
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""

    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    FRONTEND_URL: str = "http://localhost:5173"

    # Configuration pour charger le fichier .env
    model_config = SettingsConfigDict(env_file=".env")

    @model_validator(mode="after")
    def check_stripe_keys(self) -> "Settings":
        missing = []
        if not self.STRIPE_SECRET_KEY:
            missing.append("STRIPE_SECRET_KEY")
        if not self.STRIPE_WEBHOOK_SECRET:
            missing.append("STRIPE_WEBHOOK_SECRET")
        if missing:
            raise ValueError(
                f"[DÉMARRAGE IMPOSSIBLE] Variables Stripe manquantes : {', '.join(missing)}. "
                f"Ajoutez-les dans .env ou les variables d'environnement Docker."
            )
        return self

settings = Settings()