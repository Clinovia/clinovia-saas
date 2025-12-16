from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional, Tuple, List
from enum import Enum
from app.schemas.base import BaseSchema as BaseModel  # Use your BaseModelConfig
from pydantic import Field


# -----------------------------------------
# Enums
# -----------------------------------------
class PredictionStatus(str, Enum):
    """Status of the prediction."""
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"  # For cases where defaults were used


# -----------------------------------------
# Audit / Context Models
# -----------------------------------------
class ContextBase(BaseModel):
    """
    Base model with audit fields.
    Include user_id and timestamp for logging / tracking.
    """
    user_id: UUID = Field(..., description="User ID (from auth)")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Event timestamp"
    )


# -----------------------------------------
# Prediction Models
# -----------------------------------------
class PredictionRequestBase(BaseModel):
    """
    Base model for prediction requests.
    Includes audit fields and optional metadata for all prediction requests.
    """
    user_id: Optional[UUID] = None
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Request timestamp"
    )


class PredictionResponseBase(BaseModel):
    """
    Base model for predictions with metadata and error handling.
    
    All prediction responses inherit from this to ensure consistent
    structure, error reporting, and audit trails across the application.
    """
    # Unique identification
    prediction_id: UUID = Field(
        default_factory=uuid4, 
        description="Unique ID for this prediction"
    )
    
    # Model metadata
    model_version: str = Field(
        default="1.0.0",  # Changed from required to default
        description="Version of the ML model used"
    )
    
    # Status and error handling
    status: PredictionStatus = Field(
        default=PredictionStatus.SUCCESS,
        description="Status of the prediction (success/error/partial)"
    )
    
    error: Optional[str] = Field(
        None,
        description="Error message if prediction failed or encountered issues"
    )
    
    warnings: Optional[List[str]] = Field(
        None,
        description="Non-fatal warnings (e.g., 'Using default values for missing features')"
    )
    
    # Statistical metadata
    confidence_interval: Optional[Tuple[float, float]] = Field(
        None, 
        description="Optional confidence interval for the prediction (e.g., [0.3, 0.7])"
    )
    
    # Audit trail
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp when prediction was made"
    )
    
    class Config:
        json_schema_extra = {
            "success_example": {
                "prediction_id": str(uuid4()),
                "model_version": "1.0.0",
                "status": "success",
                "error": None,
                "warnings": None,
                "confidence_interval": [0.3, 0.7],
                "timestamp": "2025-01-15T10:30:00Z"
            },
            "error_example": {
                "prediction_id": str(uuid4()),
                "model_version": "1.0.0",
                "status": "error",
                "error": "Model file not found at path: models/example.pkl",
                "warnings": None,
                "confidence_interval": None,
                "timestamp": "2025-01-15T10:30:00Z"
            },
            "partial_example": {
                "prediction_id": str(uuid4()),
                "model_version": "1.0.0",
                "status": "partial",
                "error": None,
                "warnings": ["Used default value for ABETA biomarker", "Missing TAU measurement"],
                "confidence_interval": [0.25, 0.75],
                "timestamp": "2025-01-15T10:30:00Z"
            }
        }


__all__ = [
    "ContextBase",
    "PredictionRequestBase", 
    "PredictionResponseBase",
    "PredictionStatus"
]
