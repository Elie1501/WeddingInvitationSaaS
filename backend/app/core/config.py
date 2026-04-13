from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DATABASE_URL: str

    # Configuration S3
    S3_BUCKET: str = "wedding-invitations-media"
    S3_REGION: str = "eu-west-3"
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""

    # Configuration pour charger le fichier .env
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()