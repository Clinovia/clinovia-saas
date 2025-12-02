"""
Schemas for Alzheimer's 2-year progression (extended) prediction input and output.

Model: prognosis_advanced_RandomForest_best_model
Features: Clinical assessments + CSF biomarkers (ABETA, TAU, PTAU)
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, List, Optional, Union
from app.schemas.common import PredictionResponseBase


# -------------------------------------
# Input Schema
# -------------------------------------
class AlzheimerPrognosis2yrExtendedInput(BaseModel):
    """
    Input schema for extended Alzheimer's 2-year progression prediction.
    Includes clinical assessments, genetic markers, and CSF biomarkers.
    """

    patient_id: Optional[Union[str, int]] = Field(
        None, description="Patient identifier (optional)"
    )

    # Clinical/Demographic Features
    AGE: Optional[float] = Field(
        None, ge=50, le=100, description="Age of the patient in years (default: 75)"
    )

    PTGENDER: Optional[Literal["male", "female"]] = Field(
        None, description="Gender of the patient (default: female)"
    )

    PTEDUCAT: Optional[float] = Field(
        None, ge=0, le=30, description="Years of education (default: 16)"
    )

    # Cognitive Assessment Scores
    ADAS13: Optional[float] = Field(
        None, ge=0, le=85, description="ADAS13 cognitive score (default: 10.5)"
    )

    CDRSB: Optional[float] = Field(
        None, ge=0, le=18, description="Clinical Dementia Rating Sum of Boxes (default: 0.5)"
    )

    FAQ: Optional[float] = Field(
        None, ge=0, le=30, description="Functional Activities Questionnaire score (default: 0)"
    )

    GDTOTAL: Optional[float] = Field(
        None, ge=0, le=7, description="Global Deterioration Scale total score (default: 5.0)"
    )

    # Genetic Marker
    APOE4_count: Optional[int] = Field(
        None, ge=0, le=2, description="APOE4 allele count: 0, 1, or 2 (default: 0)"
    )

    # CSF Biomarkers
    ABETA: Optional[float] = Field(
        None, ge=0, description="CSF Amyloid-beta 42 level (default: 700.0)"
    )

    TAU: Optional[float] = Field(
        None, ge=0, description="CSF total Tau level (default: 300.0)"
    )

    PTAU: Optional[float] = Field(
        None, ge=0, description="CSF phosphorylated Tau level (default: 50.0)"
    )

# -------------------------------------
# Output Schema
# -------------------------------------
class AlzheimerPrognosis2yrExtendedOutput(PredictionResponseBase):
    """
    Expressive output schema for the extended 2-year Alzheimer's progression prediction.
    """

    patient_id: Optional[Union[str, int]] = Field(
        None, description="Patient identifier (echoed from input)"
    )

    model_name: str = Field(
        default="prognosis_2yr_extended_v1",
        description="Model identifier for the extended progression model"
    )

    model_version: str = Field(
        default="1.0.0",
        description="Model version"
    )

    # Probabilities
    probability_progression_to_AD_within_2yrs: Optional[float] = Field(
        None,
        description="Estimated probability of progression to Alzheimer's dementia within 2 years."
    )

    probability_stable_within_2yrs: Optional[float] = Field(
        None,
        description="Estimated probability that the patient remains stable over 2 years."
    )

    # Risk level (low, moderate, high)
    risk_level: Optional[str] = Field(
        None,
        description="Categorical risk level derived from progression probability."
    )

    # Natural language summary
    summary_text: Optional[str] = Field(
        None,
        description="Human-readable summary explaining the prognosis."
    )

    # Top contributing features
    top_features: Optional[List[str]] = Field(
        None,
        description="Top influential features contributing to the prediction."
    )

    # Error field if prediction fails
    error: Optional[str] = Field(
        None,
        description="Error message if model failed to produce a prediction."
    )