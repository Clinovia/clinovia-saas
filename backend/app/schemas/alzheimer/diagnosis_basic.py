"""
Schemas for Alzheimer's basic diagnosis model input and output.
Model: alz-diagnosis-xgboost-adni.joblib
"""

from typing import Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field, conint, confloat
from app.schemas.common import PredictionResponseBase


# -------------------------------------
# Input Schema
# -------------------------------------
class AlzheimerDiagnosisBasicInput(BaseModel):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    
    # Numeric features — names must match scaler
    AGE: confloat(gt=0) = Field(..., description="Age of the patient in years (must be >0)")
    MMSE: confloat(ge=0, le=30) = Field(..., description="Baseline Mini-Mental State Examination score (0–30)")
    FAQ: confloat(ge=0) = Field(..., description="Functional Activities Questionnaire baseline score (>=0)")
    PTEDUCAT: confloat(ge=0) = Field(..., description="Years of education (>=0)")
    RAVLT_immediate: confloat(ge=0) = Field(..., description="Rey Auditory Verbal Learning Test immediate recall baseline (>=0)")
    MOCA: confloat(ge=0, le=30) = Field(..., description="Montreal Cognitive Assessment baseline score (0–30)")
    ADAS13: confloat(ge=0) = Field(..., description="ADAS13 baseline score (>=0)")

    # Categorical features — keep as is
    PTGENDER: str = Field(..., description="Patient gender ('male' or 'female')")
    APOE4: int = Field(..., ge=-1, le=2, description="APOE4 allele count: -1=unknown, 0=none, 1=one, 2=two")



# -------------------------------------
# Output Schema
# -------------------------------------
class AlzheimerDiagnosisBasicOutput(PredictionResponseBase):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    predicted_class: Literal["CN", "MCI", "AD"] = Field(..., description="Predicted cognitive class")
    confidence: confloat(ge=0.0, le=1.0) = Field(..., description="Model confidence for predicted class (0–1)")
    probabilities: Dict[str, confloat(ge=0.0, le=1.0)] = Field(..., description="Probabilities for each cognitive class (0–1)")
    top_features: Optional[List[str]] = Field(None, description="Most influential features for prediction")
    model_name: str = Field("Alzheimer_diagnosis_with_basic_features-v1", description="Model name used for prediction")
    model_version: str = Field("1.0.0", description="Model version")

