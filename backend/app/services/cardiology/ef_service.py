"""
Ejection Fraction Service
Handles communication with the EF microservice for predictions and health checks.
"""
import os
from typing import BinaryIO, Dict, Any
from fastapi import UploadFile, HTTPException
import httpx

# -----------------------------
# Configuration
# -----------------------------
EF_SERVICE_URL = os.getenv("EF_SERVICE_URL", "http://localhost:8001")
EF_SERVICE_TOKEN = os.getenv("EF_SERVICE_TOKEN", "")
REQUEST_TIMEOUT = 120.0  # seconds


# -----------------------------
# Exceptions
# -----------------------------
class EFServiceError(Exception):
    """Custom exception for EF service errors."""
    pass


# -----------------------------
# Core Functions
# -----------------------------
async def predict_ejection_fraction(video_file: UploadFile, timeout: float = REQUEST_TIMEOUT) -> Dict[str, Any]:
    """
    Predict ejection fraction from an echocardiogram video.

    Args:
        video_file: Uploaded video file.
        timeout: Request timeout in seconds.

    Returns:
        dict: Prediction results including ef_value, severity, confidence, filename, file_size_mb, model_version.

    Raises:
        EFServiceError: For service errors or connection failures.
        HTTPException: For request validation errors.
    """
    try:
        await video_file.seek(0)

        files = {
            "video": (
                video_file.filename,
                await video_file.read(),
                video_file.content_type or "video/avi"
            )
        }

        headers = {"Authorization": f"Bearer {EF_SERVICE_TOKEN}"} if EF_SERVICE_TOKEN else {}

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(f"{EF_SERVICE_URL}/ejection-fraction", files=files, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 503:
            raise EFServiceError("EF service is starting up. Try again shortly.")
        elif response.status_code == 413:
            raise HTTPException(status_code=413, detail=response.json().get("detail", "File too large"))
        elif response.status_code == 400:
            raise HTTPException(status_code=400, detail=response.json().get("detail", "Invalid request"))
        else:
            raise EFServiceError(f"EF prediction failed: {response.json().get('detail', 'Unknown error')}")

    except httpx.TimeoutException:
        raise EFServiceError(f"EF prediction timed out after {timeout} seconds")
    except httpx.ConnectError:
        raise EFServiceError(f"Cannot connect to EF service at {EF_SERVICE_URL}")
    except httpx.HTTPError as e:
        raise EFServiceError(f"HTTP error communicating with EF service: {e}")
    except HTTPException:
        raise
    except Exception as e:
        raise EFServiceError(f"Unexpected error during EF prediction: {e}")
    finally:
        await video_file.seek(0)


async def check_ef_service_health() -> Dict[str, Any]:
    """Check if the EF microservice is healthy."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{EF_SERVICE_URL}/health")
        if response.status_code == 200:
            return response.json()
        return {"status": "unhealthy", "model_loaded": False, "error": f"Status {response.status_code}"}
    except httpx.ConnectError:
        return {"status": "unavailable", "model_loaded": False, "error": f"Cannot connect to {EF_SERVICE_URL}"}
    except Exception as e:
        return {"status": "error", "model_loaded": False, "error": str(e)}


async def get_ef_model_info() -> Dict[str, Any]:
    """Get EF model information from the microservice."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{EF_SERVICE_URL}/model-info")
        if response.status_code == 200:
            return response.json()
        raise EFServiceError(f"Failed to get model info: {response.status_code}")
    except httpx.ConnectError:
        raise EFServiceError(f"Cannot connect to EF service at {EF_SERVICE_URL}")
    except Exception as e:
        raise EFServiceError(f"Error getting model info: {e}")


# -----------------------------
# Legacy Support
# -----------------------------
async def calculate_ejection_fraction(video_file: UploadFile) -> Dict[str, Any]:
    """Legacy function name maintained for backward compatibility."""
    return await predict_ejection_fraction(video_file)
