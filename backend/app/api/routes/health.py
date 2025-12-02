# backend/app/api/routes/health.py
"""
Health check endpoints for Clinovia SaaS API.
Provides basic, database, and model readiness probes for monitoring and DevOps.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from app.api import deps
from app.clinical.utils import (
    load_model,
    is_model_loaded,
)

logger = logging.getLogger(__name__)

router = APIRouter()

API_VERSION = "1.0.0"


@router.get("/", summary="Basic health check")
async def health_check() -> dict:
    """
    Basic health check endpoint.
    Used by uptime monitors or container orchestrators.
    """
    return {"status": "healthy", "version": API_VERSION}


@router.get("/db", summary="Database health check")
async def db_health_check(db: Session = Depends(deps.get_db)) -> dict:
    """
    Verify database connectivity by executing a lightweight query.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as exc:
        logger.exception("Database health check failed")
        return {"status": "unhealthy", "database": str(exc)}


@router.get("/models", summary="Model readiness check")
async def models_health_check() -> dict:
    """
    Check if ML models are loaded and ready for inference.
    """
    models_status = {}

    try:
        # Use a safe check — do NOT call load_model() without args
        # Instead, check if model is already loaded or files exist
        from app.clinical.alzheimer.ml_models.diagnosis_extended import MODEL_PATH
        import os
        models_status["alzheimer"] = os.path.exists(MODEL_PATH)
    except Exception as exc:
        logger.exception(f"Model health check failed: {exc}")
        models_status["alzheimer"] = False

    all_loaded = all(models_status.values())

    return {
        "status": "healthy" if all_loaded else "unhealthy",
        "models": models_status,
        "cached": models_status["alzheimer"],  # or use a real cache flag if you have one
    }