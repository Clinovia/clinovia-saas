"""
Calculate CHA₂DS₂-VASc score for stroke risk stratification in atrial fibrillation.

Reference:
    Lip GYH, et al. Chest. 2010.
"""

from typing import Literal, NamedTuple
from app.schemas.cardiology import CHA2DS2VAScInput, CHA2DS2VAScOutput


# ==========================================================
# Core Logic
# ==========================================================
def calculate_cha2ds2vasc(data: CHA2DS2VAScInput) -> CHA2DS2VAScOutput:
    """
    Calculate CHA₂DS₂-VASc score and return standardized schema output.
    
    Args:
        data (CHA2DS2VAScInput): Patient input data.
    
    Returns:
        CHA2DS2VAScOutput: Structured output with score and risk category.
    """
    # Validation
    if data.age < 0:
        raise ValueError("Age must be non-negative")
    if data.gender.lower() not in {"male", "female"}:
        raise ValueError("Gender must be 'male' or 'female'")
    
    # Age-based components
    age_75_or_older = data.age >= 75
    age_65_to_74 = 65 <= data.age < 75
    
    # Calculate total score
    score = (
        int(data.congestive_heart_failure)
        + int(data.hypertension)
        + int(data.diabetes)
        + int(data.vascular_disease)
        + 2 * int(data.stroke_tia_thromboembolism)
        + 2 * int(age_75_or_older)
        + int(age_65_to_74)
        + (1 if data.gender.lower() == "female" else 0)
    )
    
    # Risk category determination
    if data.gender.lower() == "female":
        if score >= 3:
            risk_category = "high"
        elif score >= 2:
            risk_category = "moderate"
        else:
            risk_category = "low"
    else:
        if score >= 2:
            risk_category = "high"
        elif score >= 1:
            risk_category = "moderate"
        else:
            risk_category = "low"
    
    return CHA2DS2VAScOutput(
        patient_id=data.patient_id,
        score=score,
        risk_category=risk_category,
        model_name="cha2ds2vasc_rule_v1"
    )

__all__ = ["calculate_cha2ds2vasc"]