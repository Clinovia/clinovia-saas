# app/schemas/cardiology.py

"""
Schemas for Cardiology assessments using PredictionResponseBase as base:
- ASCVD risk
- Blood pressure category
- CHA2DS2-VASc score
- ECG interpretation
- Echonet EF prediction
"""

from typing import Literal, Optional, Dict, List, Union
from pydantic import BaseModel, Field
from app.schemas.common import PredictionResponseBase 

# ======================
# 1. ASCVD Risk
# ======================
class ASCVDRiskInput(BaseModel):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    age: int = Field(..., ge=40, le=79)
    gender: Literal["male", "female"]
    race: Literal["white", "black", "hispanic", "asian", "other"]
    total_cholesterol: float = Field(..., ge=130, le=320)
    hdl_cholesterol: float = Field(..., ge=20, le=100)
    systolic_bp: float = Field(..., ge=90, le=200)
    on_hypertension_treatment: bool
    smoker: bool
    diabetes: bool


class ASCVDRiskOutput(PredictionResponseBase):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    risk_percentage: float = Field(..., ge=0, le=100)
    risk_category: Literal["low", "borderline", "intermediate", "high"]
    model_name: str = Field(default="Cardiology_ascvd-v1")
    model_version: str = Field("1.0.0", description="Model version")

# ======================
# 2. Blood Pressure Category
# ======================
class BPCategoryInput(BaseModel):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    systolic_bp: float = Field(
        ..., ge=70, le=250, description="Systolic blood pressure (mmHg)"
    )
    diastolic_bp: float = Field(
        ..., ge=40, le=150, description="Diastolic blood pressure (mmHg)"
    )


class BPCategoryOutput(PredictionResponseBase):
    """Output schema for BP category classification."""
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    systolic_bp: float
    diastolic_bp: float
    category: Literal[
        "normal",
        "elevated",
        "hypertension_stage_1",
        "hypertension_stage_2",
        "hypertensive_crisis",
    ]
    model_name: str = Field(default="Cardiology_bp_category-v1")
    model_version: str = Field("1.0.0", description="Model version")

# ======================
# 3. CHA₂DS₂-VASc Score
# ======================
class CHA2DS2VAScInput(BaseModel):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    age: int = Field(..., ge=18, le=120)
    gender: Literal["male", "female"]
    congestive_heart_failure: bool
    hypertension: bool
    diabetes: bool
    stroke_tia_thromboembolism: bool
    vascular_disease: bool


class CHA2DS2VAScOutput(BaseModel):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    score: int = Field(..., ge=0, le=9)
    risk_category: Literal["low", "moderate", "high"]
    model_name: str = Field(default="Cardiology_cha2ds2vascv1")
    model_version: str = Field("1.0.0", description="Model version")
    model_config = {
        "protected_namespaces": ()  # allow all names
    }

# ======================
# 4. ECG Interpreter
# ======================
class ECGInterpretationInput(BaseModel):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    heart_rate: int = Field(..., ge=20, le=300)
    qrs_duration: int = Field(..., ge=50, le=200)
    qt_interval: Optional[int] = Field(None, ge=300, le=600)
    pr_interval: Optional[int] = Field(None, ge=80, le=400)
    rhythm: Literal["sinus", "afib", "flutter", "other"]
    st_elevation: bool = False
    t_wave_inversion: bool = False

class ECGInterpretationOutput(PredictionResponseBase):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    findings: List[str]
    rhythm: str
    overall_risk: Literal["routine", "urgent", "emergent"]
    model_name: str = Field(default="Cardiology_ecg_interpreter-v1")
    model_version: str = Field("1.0.0", description="Model version")
