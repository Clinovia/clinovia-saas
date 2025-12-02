from typing import Literal, Optional, Union

from pydantic import BaseModel, Field
from app.schemas.common import PredictionResponseBase 


class AlzheimerRiskScreenerInput(BaseModel):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    age: int = Field(..., ge=40, le=90)
    gender: Literal["male", "female"]
    education_years: int = Field(..., ge=0, le=30)
    apoe4_status: bool
    memory_score: float = Field(..., ge=0, le=30)  # e.g., MoCA or similar
    hippocampal_volume: float | None = Field(None, ge=2000, le=5000)


class AlzheimerRiskScreenerOutput(PredictionResponseBase ):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    model_name: str = "alz-risk-screener-heuristic-v1"
    model_version: str = "1.0.0"
    risk_score: float
    risk_category: Literal["low", "moderate", "high", "error"]  # match test
    recommendation: str
