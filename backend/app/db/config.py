# backend/app/db/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Database configuration.
    Supports Supabase/Postgres via DATABASE_URL environment variable.
    """
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./app.db"  # fallback for local testing
    )

    @property
    def sqlalchemy_url(self) -> str:
        """
        Ensures the URL is SQLAlchemy-compatible.
        Converts Heroku-style `postgres://` URLs to `postgresql://`.
        """
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url

settings = Settings()
