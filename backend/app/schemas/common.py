from uuid import uuid4, UUID
from datetime import datetime
from typing import Tuple, List, Optional
from enum import Enum

from pydantic import Field
from app.schemas.base import BaseSchema as BaseModel


# -----------------------------------------
# Enums
# -----------------------------------------
class PredictionStatus(str, Enum):
    """Status of the prediction."""
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"


# -----------------------------------------
# Audit / Context Models
# -----------------------------------------
class ContextBase(BaseModel):
    """
    Base model with audit fields.
    Always populated from authenticated clinician context.
    """
    clinician_id: UUID = Field(..., description="Authenticated clinician ID")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Event timestamp (UTC)",
    )


# -----------------------------------------
# Prediction Request Models
# -----------------------------------------
class PredictionRequestBase(BaseModel):
    """
    Base model for all prediction requests.

    clinician_id is REQUIRED and injected by auth middleware,
    never provided by the client.
    """
    clinician_id: UUID = Field(..., description="Authenticated clinician ID")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Request timestamp (UTC)",
    )


# -----------------------------------------
# Prediction Response Models
# -----------------------------------------
class PredictionResponseBase(BaseModel):
    """
    Base model for prediction responses with metadata,
    error handling, and auditability.
    """

    # Unique identification
    prediction_id: UUID = Field(
        default_factory=uuid4,
        description="Unique ID for this prediction",
    )

    # Model metadata
    model_version: str = Field(
        default="1.0.0",
        description="Version of the ML model used",
    )

    # Status and error handling
    status: PredictionStatus = Field(
        default=PredictionStatus.SUCCESS,
        description="Prediction execution status",
    )

    error: Optional[str] = Field(
        None,
        description="Error message if prediction failed",
    )

    warnings: Optional[List[str]] = Field(
        None,
        description="Non-fatal warnings (defaults, missing features, etc.)",
    )

    # Statistical metadata
    confidence_interval: Optional[Tuple[float, float]] = Field(
        None,
        description="Optional confidence interval [low, high]",
    )

    # Audit trail
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp when prediction was made",
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
                "timestamp": "2025-01-15T10:30:00Z",
            },
            "error_example": {
                "prediction_id": str(uuid4()),
                "model_version": "1.0.0",
                "status": "error",
                "error": "Model file not found",
                "warnings": None,
                "confidence_interval": None,
                "timestamp": "2025-01-15T10:30:00Z",
            },
            "partial_example": {
                "prediction_id": str(uuid4()),
                "model_version": "1.0.0",
                "status": "partial",
                "error": None,
                "warnings": [
                    "Used default value for ABETA biomarker",
                    "Missing TAU measurement",
                ],
                "confidence_interval": [0.25, 0.75],
                "timestamp": "2025-01-15T10:30:00Z",
            },
        }


__all__ = [
    "ContextBase",
    "PredictionRequestBase",
    "PredictionResponseBase",
    "PredictionStatus",
]
