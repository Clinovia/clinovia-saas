from typing import Dict, Literal, Optional, List, Union
from pydantic import BaseModel, Field, confloat, ConfigDict
from app.schemas.common import PredictionResponseBase 


# -----------------------------
# Input Schema
# -----------------------------
class AlzheimerDiagnosisInput(BaseModel):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    age: int = Field(..., ge=55, le=95)
    education_years: int = Field(..., ge=0, le=30)
    moca_score: float = Field(..., ge=0, le=30)
    adas13_score: float = Field(..., ge=0, le=85)
    cdr_sum: float = Field(..., ge=0, le=18)
    faq_total: int = Field(..., ge=0, le=30)
    gender: Literal["male", "female"]
    race: Literal[1, 2, 3, 4, 5, 6, 7]


# -----------------------------
# Output Schema
# -----------------------------
class AlzheimerDiagnosisOutput(PredictionResponseBase):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    model_name: str = Field("Alazheimer-diagnosis-model-v1", description="Model used for prediction")
    model_version: str = Field("1.0.0")
    predicted_class: Literal["CN", "MCI", "AD"]
    confidence: confloat(ge=0.0, le=1.0) = Field(..., description="Confidence between 0 and 1")
    probabilities: Dict[str, confloat(ge=0.0, le=1.0)]
    top_features: Optional[List[str]] = None

