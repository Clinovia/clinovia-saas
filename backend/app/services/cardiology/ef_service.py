"""
Ejection Fraction Service
Calls the EF microservice for predictions
"""
import httpx
from typing import BinaryIO, Dict, Any
from fastapi import UploadFile, HTTPException
import os

# EF Microservice URL - can be configured via environment variable
EF_SERVICE_URL = os.environ.get(
    "EF_SERVICE_URL", 
    "http://localhost:8081"  # Default for local development
)

# Timeout for microservice calls (in seconds)
REQUEST_TIMEOUT = 120.0  # 2 minutes for video processing


class EFServiceError(Exception):
    """Custom exception for EF service errors"""
    pass


async def predict_ejection_fraction(
    video_file: UploadFile,
    timeout: float = REQUEST_TIMEOUT
) -> Dict[str, Any]:
    """
    Predict ejection fraction from echocardiogram video.
    
    Args:
        video_file: Uploaded video file
        timeout: Request timeout in seconds
        
    Returns:
        dict: Prediction results containing:
            - ef_value (float): Predicted EF percentage
            - severity (str): Clinical severity classification
            - confidence (float, optional): Model confidence
            - filename (str): Original filename
            - file_size_mb (float): File size
            - model_version (str): Model version used
            
    Raises:
        EFServiceError: If the microservice is unavailable or returns an error
        HTTPException: If validation fails
    """
    try:
        # Reset file pointer to beginning
        await video_file.seek(0)
        
        # Prepare the file for multipart upload
        files = {
            "video": (
                video_file.filename,
                await video_file.read(),
                video_file.content_type or "video/avi"
            )
        }
        
        # Call the microservice
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{EF_SERVICE_URL}/predict-ef",
                files=files
            )
            
            # Handle different response codes
            if response.status_code == 200:
                return response.json()
            
            elif response.status_code == 503:
                # Service starting up
                raise EFServiceError(
                    "EF prediction service is starting up. Please try again in a moment."
                )
            
            elif response.status_code == 413:
                # File too large
                error_detail = response.json().get("detail", "File too large")
                raise HTTPException(status_code=413, detail=error_detail)
            
            elif response.status_code == 400:
                # Validation error
                error_detail = response.json().get("detail", "Invalid request")
                raise HTTPException(status_code=400, detail=error_detail)
            
            else:
                # Other errors
                error_detail = response.json().get("detail", "Prediction failed")
                raise EFServiceError(f"EF prediction failed: {error_detail}")
                
    except httpx.TimeoutException:
        raise EFServiceError(
            f"EF prediction timed out after {timeout} seconds. "
            "Video may be too large or complex."
        )
    
    except httpx.ConnectError:
        raise EFServiceError(
            f"Cannot connect to EF service at {EF_SERVICE_URL}. "
            "Please ensure the microservice is running."
        )
    
    except httpx.HTTPError as e:
        raise EFServiceError(f"HTTP error communicating with EF service: {e}")
    
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    
    except Exception as e:
        raise EFServiceError(f"Unexpected error during EF prediction: {e}")
    
    finally:
        # Reset file pointer for potential reuse
        await video_file.seek(0)


async def check_ef_service_health() -> Dict[str, Any]:
    """
    Check if the EF microservice is healthy and ready.
    
    Returns:
        dict: Health status with model_loaded flag
        
    Raises:
        EFServiceError: If service is unreachable
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{EF_SERVICE_URL}/health")
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "status": "unhealthy",
                    "model_loaded": False,
                    "error": f"Service returned status {response.status_code}"
                }
                
    except httpx.ConnectError:
        return {
            "status": "unavailable",
            "model_loaded": False,
            "error": f"Cannot connect to {EF_SERVICE_URL}"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "model_loaded": False,
            "error": str(e)
        }


async def get_ef_model_info() -> Dict[str, Any]:
    """
    Get information about the EF model from the microservice.
    
    Returns:
        dict: Model configuration details
        
    Raises:
        EFServiceError: If service is unreachable
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{EF_SERVICE_URL}/model-info")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise EFServiceError(
                    f"Failed to get model info: {response.status_code}"
                )
                
    except httpx.ConnectError:
        raise EFServiceError(
            f"Cannot connect to EF service at {EF_SERVICE_URL}"
        )
    
    except Exception as e:
        raise EFServiceError(f"Error getting model info: {e}")


# Backward compatibility with old function name
async def calculate_ejection_fraction(video_file: UploadFile) -> Dict[str, Any]:
    """
    Legacy function name - calls predict_ejection_fraction.
    Maintained for backward compatibility.
    """
    return await predict_ejection_fraction(video_file)