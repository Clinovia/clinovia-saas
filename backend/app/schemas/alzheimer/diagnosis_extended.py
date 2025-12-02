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
    MMSE_bl: confloat(ge=0, le=30) = Field(..., description="Baseline Mini-Mental State Examination score (0–30)")
    CDRSB_bl: confloat(ge=0) = Field(..., description="Baseline Clinical Dementia Rating Sum of Boxes (>=0)")
    FAQ_bl: confloat(ge=0) = Field(..., description="Functional Activities Questionnaire baseline score (>=0)")
    PTEDUCAT: confloat(ge=0) = Field(..., description="Years of education (>=0)")
    PTGENDER: Literal["male", "female"] = Field(..., description="Gender of the patient")
    APOE4: conint(ge=0, le=2) = Field(..., description="APOE4 allele count (0, 1, or 2)")
    RAVLT_immediate_bl: confloat(ge=0) = Field(..., description="Rey Auditory Verbal Learning Test immediate recall baseline (>=0)")
    MOCA_bl: confloat(ge=0, le=30) = Field(..., description="Montreal Cognitive Assessment baseline score (0–30)")
    ADAS13_bl: confloat(ge=0) = Field(..., description="ADAS13 baseline score (>=0)")

    # Imaging & biomarker features (optional)
    Hippocampus_bl: Optional[confloat(ge=0)] = Field(None, description="Baseline hippocampal volume (>=0)")
    Ventricles_bl: Optional[confloat(ge=0)] = Field(None, description="Baseline ventricular volume (>=0)")
    WholeBrain_bl: Optional[confloat(ge=0)] = Field(None, description="Baseline whole brain volume (>=0)")
    Entorhinal_bl: Optional[confloat(ge=0)] = Field(None, description="Baseline entorhinal cortex volume (>=0)")
    FDG_bl: Optional[confloat(ge=0)] = Field(None, description="Baseline FDG-PET standardized uptake value ratio (>=0)")
    AV45_bl: Optional[confloat(ge=0)] = Field(None, description="Amyloid PET (AV45 tracer) baseline value (>=0)")
    PIB_bl: Optional[confloat(ge=0)] = Field(None, description="Amyloid PET (PIB tracer) baseline value (>=0)")
    FBB_bl: Optional[confloat(ge=0)] = Field(None, description="Amyloid PET (FBB tracer) baseline value (>=0)")
    ABETA_bl: Optional[confloat(ge=0)] = Field(None, description="Baseline CSF Aβ42 level (>=0)")
    TAU_bl: Optional[confloat(ge=0)] = Field(None, description="Baseline CSF total tau level (>=0)")
    PTAU_bl: Optional[confloat(ge=0)] = Field(None, description="Baseline CSF phosphorylated tau level (>=0)")
    mPACCdigit_bl: Optional[confloat()] = Field(None, description="Modified Preclinical Alzheimer Cognitive Composite – Digit")
    mPACCtrailsB_bl: Optional[confloat()] = Field(None, description="Modified Preclinical Alzheimer Cognitive Composite – Trails B")

# -------------------------------------
# Output Schema
# -------------------------------------
class AlzheimerDiagnosisExtendedOutput(PredictionResponseBase):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    model_name: str = Field("Alzheimer-diagnosis-with-extended-features-v1", description="Model used for prediction")
    model_version: str = Field("1.0.0", description="Model version")
    predicted_class: Literal["CN", "MCI", "AD"] = Field(..., description="Predicted cognitive class")
    confidence: confloat(ge=0.0, le=1.0) = Field(..., description="Model confidence for predicted class (0–1)")
    probabilities: Dict[str, confloat(ge=0.0, le=1.0)] = Field(..., description="Probabilities for each cognitive class (0–1)")
    top_features: Optional[List[str]] = Field(None, description="Most influential features for prediction")
