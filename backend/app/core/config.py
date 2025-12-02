"""
Application configuration settings.
"""
import os
import json
from typing import List
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.engine.url import URL


class Settings:
    """Application settings with support for testing mode."""
    
    # General
    PROJECT_NAME: str = "Clinovia"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # Testing flag
    TESTING: bool = os.getenv("TESTING", "False").lower() == "true"
    
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
    
    # PostgreSQL - default to values in .env
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "clinovia_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "clinovia_pass")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "clinovia_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    # Stripe
    STRIPE_API_KEY: str = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")
    
    # API prefix
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = json.loads(
        os.getenv(
            "BACKEND_CORS_ORIGINS",
            '["http://localhost", "http://localhost:3000"]'
        )
    )
    
    @property
    def DATABASE_URL(self) -> str:
        """
        SQLAlchemy database URL.
        Returns in-memory SQLite URL when in testing mode.
        """
        # Use SQLite for testing
        if self.TESTING:
            return "sqlite:///:memory:"
        
        # Use explicit DATABASE_URL if provided (for production/staging)
        explicit_url = os.getenv("DATABASE_URL")
        if explicit_url:
            # Handle Heroku postgres:// vs postgresql://
            if explicit_url.startswith("postgres://"):
                explicit_url = explicit_url.replace("postgres://", "postgresql://", 1)
            return explicit_url
        
        # Otherwise construct from components
        return str(
            URL.create(
                drivername="postgresql+psycopg2",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                database=self.POSTGRES_DB,
            )
        )


settings = Settings()