"""
Schemas for Alzheimer's basic diagnosis model input and output.
Model: alz-diagnosis-xgboost-adni.joblib
Features: BASIC_FEATURE_ORDER = [
    "AGE", "MMSE_bl", "CDRSB_bl", "FAQ_bl", "PTEDUCAT",
    "PTGENDER", "APOE4", "RAVLT_immediate_bl", "MOCA_bl", "ADAS13_bl"
]
"""

from typing import Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field, conint, confloat
from app.schemas.common import PredictionResponseBase


# -------------------------------------
# Input Schema
# -------------------------------------
class AlzheimerDiagnosisBasicInput(BaseModel):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    AGE: confloat(gt=0) = Field(..., description="Age of the patient in years (must be >0)")
    MMSE_bl: confloat(ge=0, le=30) = Field(..., description="Baseline Mini-Mental State Examination score (0–30)")
    CDRSB_bl: confloat(ge=0) = Field(..., description="Baseline Clinical Dementia Rating Sum of Boxes (>=0)")
    FAQ_bl: confloat(ge=0) = Field(..., description="Functional Activities Questionnaire baseline score (>=0)")
    PTEDUCAT: confloat(ge=0) = Field(..., description="Years of education (>=0)")
    PTGENDER: str = Field(..., description="Patient gender ('male' or 'female')")  # ← ADD THIS
    APOE4: int = Field(..., ge=-1, le=2, description="APOE4 allele count: -1=unknown, 0=none, 1=one, 2=two")  # ← ADD THIS
    RAVLT_immediate_bl: confloat(ge=0) = Field(..., description="Rey Auditory Verbal Learning Test immediate recall baseline (>=0)")
    MOCA_bl: confloat(ge=0, le=30) = Field(..., description="Montreal Cognitive Assessment baseline score (0–30)")
    ADAS13_bl: confloat(ge=0) = Field(..., description="ADAS13 baseline score (>=0)")


# -------------------------------------
# Output Schema
# -------------------------------------
class AlzheimerDiagnosisBasicOutput(PredictionResponseBase):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    model_name: str = Field("Alzheimer-diagnosis-with-basic-features-v1", description="Model name used for prediction")
    model_version: str = Field("1.0.0", description="Model version")
    predicted_class: Literal["CN", "MCI", "AD"] = Field(..., description="Predicted cognitive class")
    confidence: confloat(ge=0.0, le=1.0) = Field(..., description="Model confidence for predicted class (0–1)")
    probabilities: Dict[str, confloat(ge=0.0, le=1.0)] = Field(..., description="Probabilities for each cognitive class (0–1)")
    top_features: Optional[List[str]] = Field(None, description="Most influential features for prediction")

