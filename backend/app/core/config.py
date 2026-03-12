# bacnkend/app/core/config.py

"""
Application configuration settings.
Optimized for Supabase-authenticated FastAPI services.
"""

import os
import json
from typing import List, Optional


class Settings:
    """
    Centralized application settings.

    Design principles:
    - Environment-driven
    - Verification-only JWT (Supabase)
    - No token issuance
    - Explicit dev / prod separation
    """

    # ------------------------------------------------------------------
    # Environment
    # ------------------------------------------------------------------

    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    TESTING: bool = os.getenv("TESTING", "false").lower() == "true"

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    PROJECT_NAME: str = "Clinovia"
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")

    # ------------------------------------------------------------------
    # Supabase (JWT verification only)
    # ------------------------------------------------------------------

    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")

    # JWT verification parameters
    SUPABASE_JWT_AUDIENCE: str = os.getenv(
        "SUPABASE_JWT_AUD", "authenticated"
    )
    SUPABASE_JWT_ISSUER: str = os.getenv(
        "SUPABASE_JWT_ISSUER", ""
    )
    SUPABASE_JWT_PUBLIC_KEY: str = os.getenv(
        "SUPABASE_JWT_PUBLIC_KEY", ""
    )

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------

    BACKEND_CORS_ORIGINS: List[str] = json.loads(
        os.getenv(
            "BACKEND_CORS_ORIGINS",
            '["http://localhost:3000","http://127.0.0.1:3000"]'
        )
    )

    # ------------------------------------------------------------------
    # Safety checks
    # ------------------------------------------------------------------

    def validate(self) -> None:
        """
        Validate critical settings at startup.
        Prevents half-configured deployments.
        """
        if self.ENV == "production":
            assert self.SUPABASE_URL, "SUPABASE_URL must be set in production"
            assert (
                self.SUPABASE_JWT_PUBLIC_KEY
            ), "SUPABASE_JWT_PUBLIC_KEY must be set in production"


# ----------------------------------------------------------------------
# Singleton settings instance
# ----------------------------------------------------------------------

settings = Settings()
settings.validate()
__all__ = ["settings"]
