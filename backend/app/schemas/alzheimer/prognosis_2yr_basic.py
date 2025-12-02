# app/schemas/alzheimer/prognosis_2yr_basic.py

"""
Schemas for Alzheimer's 2-year progression (basic) prediction input and output.
Model: progress_basic_model
Features: PROGRESS_BASIC_FEATURES
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Dict, List, Optional, Union
from app.schemas.common import PredictionResponseBase 


# -------------------------------------
# Input Schema
# -------------------------------------
class AlzheimerPrognosis2yrBasicInput(BaseModel):
    patient_id: Optional[Union[str, int]] = Field(None, description="Patient identifier")
    AGE: float = Field(..., description="Age of the patient in years")
    PTGENDER: Literal["male", "female"] = Field(..., description="Gender of the patient")
    PTEDUCAT: float = Field(..., description="Years of education")
    ADAS13: float = Field(..., description="ADAS13 score")
    MOCA: float = Field(..., description="Montreal Cognitive Assessment score")
    CDRSB: float = Field(..., description="Clinical Dementia Rating Sum of Boxes")
    FAQ: float = Field(..., description="Functional Activities Questionnaire score")
    APOE4_count: int = Field(..., ge=0, le=2, description="APOE4 allele count (0, 1, or 2)")
    GDTOTAL: float = Field(..., description="Global Deterioration Scale total score")

# -------------------------------------
# Output Schema
# -------------------------------------
class AlzheimerPrognosis2yrBasicOutput(PredictionResponseBase):
    patient_id: Optional[Union[str, int]] = None

    model_name: str = Field(
        "prognosis_2yr_basic_v1",
        description="Model filename used for prediction"
    )
    model_version: str = Field(
        "1.0.0",
        description="Model version"
    )

    # Backend returns these explicitly
    probability_progression_to_AD_within_2yrs: Optional[float] = Field(
        None, description="Probability the condition progresses within 2 years"
    )
    probability_stable_within_2yrs: Optional[float] = Field(
        None, description="Probability the condition remains stable"
    )

    # ⭐ REQUIRED: frontend uses this → must exist
    risk_level: Optional[str] = Field(
        None, description="Computed risk level: low, moderate, high"
    )

    summary_text: Optional[str] = Field(
        None, description="Natural language summary of risk"
    )

    top_features: Optional[List[str]] = Field(
        None, description="Most influential features for prediction"
    )