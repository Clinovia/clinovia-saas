"""
Application configuration settings, Supabase-ready.
"""
import os
import json
from typing import List
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.engine.url import URL

class Settings:
    """Application settings with support for testing mode and Supabase integration."""

    # --- General ---
    PROJECT_NAME: str = "Clinovia"
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "super-secret-key-change-in-production"
    )
    ALGORITHM: str = "HS256"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    TESTING: bool = os.getenv("TESTING", "False").lower() == "true"

    # --- OAuth2 (for Supabase JWTs) ---
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    # --- Supabase ---
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY", "")

    # --- Stripe ---
    STRIPE_API_KEY: str = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")

    # --- API ---
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")

    # --- CORS ---
    BACKEND_CORS_ORIGINS: List[str] = json.loads(
        os.getenv(
            "BACKEND_CORS_ORIGINS",
            '["http://localhost", "http://localhost:3000"]'
        )
    )

    # --- Ejection Fraction service ---
    EF_SERVICE_URL: str = os.getenv("EF_SERVICE_URL", "http://localhost:8081")
    EF_SERVICE_TIMEOUT: float = float(os.getenv("EF_SERVICE_TIMEOUT", 120.0))

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL(self) -> str:
        """
        Returns the SQLAlchemy database URL.
        - SQLite in-memory for testing.
        - Supabase DATABASE_URL if provided.
        - Otherwise build from components (fallback).
        """
        if self.TESTING:
            return "sqlite:///:memory:"

        # Use explicit DATABASE_URL first (Supabase)
        explicit_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DATABASE_URL")
        if explicit_url:
            # Convert Heroku-style URL if needed
            if explicit_url.startswith("postgres://"):
                explicit_url = explicit_url.replace(
                    "postgres://", "postgresql+psycopg2://", 1
                )
            return explicit_url

        # Fallback to components (local dev)
        return str(
            URL.create(
                drivername="postgresql+psycopg2",
                username=os.getenv("POSTGRES_USER", "clinovia_user"),
                password=os.getenv("POSTGRES_PASSWORD", "clinovia_pass"),
                host=os.getenv("POSTGRES_HOST", "localhost"),
                port=os.getenv("POSTGRES_PORT", "5432"),
                database=os.getenv("POSTGRES_DB", "clinovia_db"),
            )
        )


# Single settings instance to use everywhere
settings = Settings()
