# backend/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "sqlite:///./gridex.db"

    CARD_NUMBER: str = "0000 0000 0000 0000"

    LOCK_MINUTES: int = 5
    BASE_RATE: float = 0.0105
    FEE_PCT: float = 0.01

    CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
