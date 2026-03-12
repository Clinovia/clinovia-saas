"""
Health check endpoints for Clinovia SaaS API (Supabase-only).

Provides:
- Basic liveness check
- Supabase connectivity check
- ML model readiness check

Safe for ALB, uptime monitors, and container orchestration.
"""

from fastapi import APIRouter
import logging
import httpx
import os

from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])

API_VERSION = "1.0.0"


# ================================================================
# Basic health check
# ================================================================

@router.get("/", summary="Basic health check")
async def health_check() -> dict:
    """
    Liveness probe.
    """
    return {
        "status": "healthy",
        "version": API_VERSION,
    }


# ================================================================
# Supabase connectivity check
# ================================================================

@router.get("/supabase", summary="Supabase connectivity check")
async def supabase_health_check() -> dict:
    """
    Verifies Supabase is reachable (auth service).
    """
    try:
        url = settings.SUPABASE_URL
        if not url.startswith("http"):
            url = "https://" + url.lstrip("/")

        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{url}/auth/v1/health")

        return {
            "status": "healthy" if resp.status_code == 200 else "unhealthy",
            "supabase_status_code": resp.status_code,
        }

    except Exception as exc:
        logger.exception("Supabase health check failed")
        return {
            "status": "unhealthy",
            "error": str(exc),
        }


# ================================================================
# ML model readiness check
# ================================================================

@router.get("/models", summary="Model readiness check")
async def models_health_check() -> dict:
    """
    Check whether required ML model artifacts exist on disk.
    Does NOT load models into memory.
    """
    models_status = {}

    try:
        from app.clinical.alzheimer.ml_models.diagnosis_extended import MODEL_PATH
        models_status["alzheimer_diagnosis_extended"] = os.path.exists(MODEL_PATH)
    except Exception as exc:
        logger.exception("Alzheimer model health check failed")
        models_status["alzheimer_diagnosis_extended"] = False

    all_ready = all(models_status.values())

    return {
        "status": "healthy" if all_ready else "unhealthy",
        "models": models_status,
    }
