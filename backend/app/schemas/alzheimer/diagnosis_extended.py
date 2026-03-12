"""
Schemas for Alzheimer's extended diagnosis model input and output.
Includes cognitive, demographic, imaging, and biomarker features.

Model: alz-diagnosis-xgboost-advanced.joblib
Features include:
BASIC_FEATURE_ORDER + imaging & biomarker fields
"""

from typing import Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field, conint, confloat
from app.schemas.common import PredictionResponseBase


# -------------------------------------
# Input Schema
# -------------------------------------
class AlzheimerDiagnosisExtendedInput(BaseModel):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")

    # Basic cognitive & demographic features
    AGE: confloat(gt=0) = Field(..., description="Age of the patient in years (must be >0)")
    MMSE: confloat(ge=0, le=30) = Field(..., description="Baseline Mini-Mental State Examination score (0–30)")
    FAQ: confloat(ge=0) = Field(..., description="Functional Activities Questionnaire baseline score (>=0)")
    PTEDUCAT: confloat(ge=0) = Field(..., description="Years of education (>=0)")
    PTGENDER: Literal["male", "female"] = Field(..., description="Gender of the patient")
    APOE4: conint(ge=0, le=2) = Field(..., description="APOE4 allele count (0, 1, or 2)")
    RAVLT_immediate: confloat(ge=0) = Field(..., description="Rey Auditory Verbal Learning Test immediate recall baseline (>=0)")
    MOCA: confloat(ge=0, le=30) = Field(..., description="Montreal Cognitive Assessment baseline score (0–30)")
    ADAS13: confloat(ge=0) = Field(..., description="ADAS13 baseline score (>=0)")

    # Imaging & biomarker features (optional)
    Hippocampus: Optional[confloat(ge=0)] = Field(None, description="Baseline hippocampal volume (>=0)")
    Ventricles: Optional[confloat(ge=0)] = Field(None, description="Baseline ventricular volume (>=0)")
    WholeBrain: Optional[confloat(ge=0)] = Field(None, description="Baseline whole brain volume (>=0)")
    Entorhinal: Optional[confloat(ge=0)] = Field(None, description="Baseline entorhinal cortex volume (>=0)")
    FDG: Optional[confloat(ge=0)] = Field(None, description="Baseline FDG-PET standardized uptake value ratio (>=0)")
    AV45: Optional[confloat(ge=0)] = Field(None, description="Amyloid PET (AV45 tracer) baseline value (>=0)")
    PIB: Optional[confloat(ge=0)] = Field(None, description="Amyloid PET (PIB tracer) baseline value (>=0)")
    FBB: Optional[confloat(ge=0)] = Field(None, description="Amyloid PET (FBB tracer) baseline value (>=0)")
    ABETA: Optional[confloat(ge=0)] = Field(None, description="Baseline CSF Aβ42 level (>=0)")
    TAU: Optional[confloat(ge=0)] = Field(None, description="Baseline CSF total tau level (>=0)")
    PTAU: Optional[confloat(ge=0)] = Field(None, description="Baseline CSF phosphorylated tau level (>=0)")
    mPACCdigit: Optional[confloat()] = Field(None, description="Modified Preclinical Alzheimer Cognitive Composite – Digit")
    mPACCtrailsB: Optional[confloat()] = Field(None, description="Modified Preclinical Alzheimer Cognitive Composite – Trails B")

# -------------------------------------
# Output Schema
# -------------------------------------
class AlzheimerDiagnosisExtendedOutput(PredictionResponseBase):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    predicted_class: Literal["CN", "MCI", "AD"] = Field(..., description="Predicted cognitive class")
    confidence: confloat(ge=0.0, le=1.0) = Field(..., description="Model confidence for predicted class (0–1)")
    probabilities: Dict[str, confloat(ge=0.0, le=1.0)] = Field(..., description="Probabilities for each cognitive class (0–1)")
    top_features: Optional[List[str]] = Field(None, description="Most influential features for prediction")
    model_name: str = Field("Alzheimer_diagnosis_with_extended_features-v1", description="Model used for prediction")
    model_version: str = Field("1.0.0", description="Model version")
