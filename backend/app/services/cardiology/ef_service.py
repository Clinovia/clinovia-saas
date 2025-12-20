# backend/app/services/cardiology/ef_service.py
"""
Ejection Fraction Service
Handles communication with the EF microservice and integrates
with the standard assessment pipeline.
"""

import os
from typing import Dict, Any, Optional
from uuid import UUID

import httpx
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.schemas.cardiology import EchonetEFOutput, EchonetEFInput
from app.db.models.assessments import AssessmentType
from app.services.assessment_pipeline import run_assessment_pipeline


# ================================================================
# Configuration
# ================================================================

EF_SERVICE_URL = os.getenv("EF_SERVICE_URL", "http://localhost:8081")
EF_SERVICE_TOKEN = os.getenv("EF_SERVICE_TOKEN", "")
REQUEST_TIMEOUT = 120.0  # seconds


# ================================================================
# Exceptions
# ================================================================

class EFServiceError(Exception):
    """Custom exception for EF service errors."""
    pass


# ================================================================
# Internal: Microservice Call
# ================================================================

async def _call_ef_microservice(
    video_file: UploadFile,
    timeout: float = REQUEST_TIMEOUT,
) -> Dict[str, Any]:
    """
    Calls the EF microservice and returns raw prediction output.
    """
    try:
        await video_file.seek(0)

        files = {
            "video": (
                video_file.filename,
                await video_file.read(),
                video_file.content_type or "video/avi",
            )
        }

        headers = {"Authorization": f"Bearer {EF_SERVICE_TOKEN}"} if EF_SERVICE_TOKEN else {}

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{EF_SERVICE_URL}/ejection-fraction",
                files=files,
                headers=headers,
            )

        if response.status_code == 200:
            return response.json()
        if response.status_code == 503:
            raise EFServiceError("EF service is warming up. Try again shortly.")
        if response.status_code in (400, 413):
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json().get("detail", "Invalid EF request"),
            )
        raise EFServiceError(f"EF prediction failed: {response.json().get('detail', 'Unknown error')}")
    except httpx.TimeoutException:
        raise EFServiceError(f"EF prediction timed out after {timeout} seconds")
    except httpx.ConnectError:
        raise EFServiceError(f"Cannot connect to EF service at {EF_SERVICE_URL}")
    except httpx.HTTPError as e:
        raise EFServiceError(f"HTTP error communicating with EF service: {e}")
    finally:
        await video_file.seek(0)


# ================================================================
# Public: Assessment Pipeline Entry
# ================================================================

async def run_ef_prediction(
    *,
    video: UploadFile,
    db: Session,
    clinician_id: UUID,
    patient_id: Optional[str] = None,
) -> EchonetEFOutput:
    """
    Full EF prediction pipeline:
    - calls microservice
    - normalizes output
    - persists assessment
    - returns EchonetEFOutput
    """
    raw = await _call_ef_microservice(video)

    # Normalize microservice output → schema fields
    model_output = {
        "patient_id": patient_id,
        "ef_percent": raw.get("ef_value"),
        "category": raw.get("severity"),
        "confidence": raw.get("confidence"),
        "warnings": raw.get("warnings"),
        "model_name": raw.get("model_name", "echonet_3dcnn"),
        "model_version": raw.get("model_version", "1.0.0"),
    }

    # Create input schema instance
    input_schema = EchonetEFInput(video_file=video.filename)

    return run_assessment_pipeline(
        input_schema=input_schema,
        db=db,
        clinician_id=clinician_id,
        patient_id=patient_id,
        model_function=lambda _: model_output,
        assessment_type=AssessmentType.CARDIOLOGY_EJECTION_FRACTION,
        specialty="cardiology",
        model_name=model_output["model_name"],
        model_version=model_output["model_version"],
        use_cache=False,
    )


# ================================================================
# Health & Metadata
# ================================================================

async def check_ef_service_health() -> Dict[str, Any]:
    """Check EF microservice health."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{EF_SERVICE_URL}/health")
        return response.json() if response.status_code == 200 else {"status": "unhealthy", "error": f"Status {response.status_code}"}
    except Exception as e:
        return {"status": "unavailable", "error": str(e)}


async def get_ef_model_info() -> Dict[str, Any]:
    """Retrieve EF model metadata."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{EF_SERVICE_URL}/model-info")
        if response.status_code == 200:
            return response.json()
        raise EFServiceError(f"Failed to get model info: {response.status_code}")
    except Exception as e:
        raise EFServiceError(f"Error getting model info: {e}")


# ================================================================
# Legacy Support
# ================================================================

async def calculate_ejection_fraction(video_file: UploadFile) -> Dict[str, Any]:
    """
    Legacy alias (do not use in new code).
    """
    return await _call_ef_microservice(video_file)
