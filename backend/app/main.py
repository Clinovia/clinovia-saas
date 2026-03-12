"""
Main FastAPI application entry point.
Supabase-only (auth.users only, no public.users).
"""

# ------------------------------------------------------------------
# Environment loading (MUST be first)
# ------------------------------------------------------------------

from dotenv import load_dotenv
load_dotenv()

# ------------------------------------------------------------------
# Standard imports
# ------------------------------------------------------------------

import logging
from contextlib import asynccontextmanager
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------------------------------------------
# Core imports
# ------------------------------------------------------------------

from app.core.config import settings
from app.core.http import async_client
from app.core.supabase_client import supabase

from app.core.middleware.request_id_middleware import RequestIDMiddleware
from app.core.middleware.error_handling_middleware import ErrorHandlingMiddleware

# ------------------------------------------------------------------
# API routers
# ------------------------------------------------------------------

from app.api.routes import health, cardiology_reports, alzheimer_reports
from app.api.routes.auto_assessments import register_assessment_routes

# ------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------

APP_VERSION = "1.0.0"
LOGGER_NAME = "clinovia"

logger = logging.getLogger(LOGGER_NAME)


# ------------------------------------------------------------------
# Global application state
# ------------------------------------------------------------------

class AppState:
    models_loaded: bool = False


state = AppState()


# ------------------------------------------------------------------
# Database health check
# ------------------------------------------------------------------

def check_database() -> bool:
    """
    Lightweight Supabase connectivity check.
    """

    try:
        supabase.table("assessments").select("id").limit(1).execute()
        return True

    except Exception as exc:

        logger.error(
            {
                "event": "supabase_health_check_failed",
                "error": str(exc),
            }
        )

        return False


# ------------------------------------------------------------------
# Lifespan
# ------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        {
            "event": "startup_initiated",
            "environment": settings.ENV,
            "testing": settings.TESTING,
            "version": APP_VERSION,
        }
    )

    # ------------------------------------------------
    # Startup
    # ------------------------------------------------

    try:

        # Load ML models or heavy resources here
        state.models_loaded = True

        logger.info(
            {
                "event": "models_loaded",
                "status": "success",
            }
        )

    except Exception as exc:

        state.models_loaded = False

        logger.error(
            {
                "event": "model_load_failed",
                "error": str(exc),
            }
        )

    logger.info({"event": "startup_complete"})

    yield

    # ------------------------------------------------
    # Shutdown
    # ------------------------------------------------

    logger.info({"event": "shutdown_initiated"})

    try:
        await async_client.aclose()
    except Exception as exc:
        logger.warning(
            {
                "event": "http_client_shutdown_failed",
                "error": str(exc),
            }
        )


# ------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------

def register_middleware(app: FastAPI) -> None:

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)


# ------------------------------------------------------------------
# Infrastructure routes
# ------------------------------------------------------------------

def register_infrastructure_routes(app: FastAPI) -> None:

    @app.get("/health", tags=["Infrastructure"])
    def liveness() -> Dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready", tags=["Infrastructure"])
    def readiness() -> Dict[str, object]:

        db_ok = check_database()

        return {
            "status": "ready" if (db_ok and state.models_loaded) else "not_ready",
            "models_loaded": state.models_loaded,
            "database_connected": db_ok,
            "version": APP_VERSION,
        }


# ------------------------------------------------------------------
# API routers
# ------------------------------------------------------------------

def register_api_routes(app: FastAPI) -> None:

    # Static routers
    routers = [
        (health.router, f"{settings.API_V1_STR}/health"),
        (cardiology_reports.router, f"{settings.API_V1_STR}/cardiology/reports"),
        (alzheimer_reports.router, f"{settings.API_V1_STR}/alzheimer/reports"),
    ]

    for router, prefix in routers:
        app.include_router(router, prefix=prefix)

    # ------------------------------------------------
    # Auto-generated assessment routes
    # ------------------------------------------------

    specialty_routers = register_assessment_routes()

    for specialty, router in specialty_routers.items():
        app.include_router(router, prefix=settings.API_V1_STR)


# ------------------------------------------------------------------
# Root endpoint
# ------------------------------------------------------------------

def register_root(app: FastAPI):

    @app.get("/", tags=["Root"])
    def root():

        return {
            "service": settings.PROJECT_NAME,
            "version": APP_VERSION,
            "environment": settings.ENV,
        }


# ------------------------------------------------------------------
# App factory
# ------------------------------------------------------------------

def create_app() -> FastAPI:

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=APP_VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan,
    )

    register_middleware(app)
    register_infrastructure_routes(app)
    register_api_routes(app)
    register_root(app)

    return app


# ------------------------------------------------------------------
# App instance
# ------------------------------------------------------------------

app = create_app()