# app/clinical/alzheimer/ml_models/risk_screener.py

"""
Rule-based Alzheimer's Risk Screener
------------------------------------
Performs rule-based scoring and risk categorization using clinical factors.
Refactored for schema-based consistency and maintainability.
"""

from app.schemas.alzheimer.risk_screener import (
    AlzheimerRiskScreenerInput,
    AlzheimerRiskScreenerOutput,
)
from app.clinical.utils import log_usage


def calculate_risk_score(
    input_schema: AlzheimerRiskScreenerInput,
) -> AlzheimerRiskScreenerOutput:
    """
    Calculate Alzheimer's risk using a rule-based clinical screener.
    
    Based on CAIDE/ANU-ADRI risk factors: age, APOE4, memory, education, sex, and optional biomarkers.
    Returns a risk score (0.0–0.90), category (low/moderate/high), and clinical recommendation.
    """
    input_data = input_schema.dict()

    try:
        age = input_data["age"]
        gender = input_data["gender"]  # 'male' or 'female'
        education_years = input_data["education_years"]
        apoe4_status = input_data["apoe4_status"]  # bool
        memory_score = input_data["memory_score"]  # e.g., MoCA (0–30)
        hippocampal_volume = input_data.get("hippocampal_volume")  # optional

        # Start with baseline risk (~2–3% for low-risk 55yo)
        risk = 0.03

        # === Age (strongest predictor) ===
        if age >= 80:
            risk += 0.40
        elif age >= 75:
            risk += 0.30
        elif age >= 70:
            risk += 0.20
        elif age >= 65:
            risk += 0.10
        # <65: minimal added risk

        # === APOE4 status ===
        if apoe4_status:
            risk += 0.25  # Hetero- or homozygous — simplified here

        # === Gender ===
        if gender == "female":
            risk += 0.05  # Higher lifetime risk post-menopause

        # === Education (protective) ===
        if education_years < 8:
            risk += 0.15  # Low education = higher risk
        elif education_years < 12:
            risk += 0.08
        elif education_years >= 16:
            risk -= 0.05  # Protective effect

        # === Memory score (MoCA-like; 0–30) ===
        if memory_score <= 18:
            risk += 0.25  # Likely MCI/early dementia
        elif memory_score <= 22:
            risk += 0.15
        elif memory_score <= 25:
            risk += 0.05
        # >25: normal cognition → no added risk

        # === Hippocampal volume (optional; in mm³) ===
        if hippocampal_volume is not None:
            # Normal volume: ~3000–4000 mm³ for cognitively normal elderly
            if hippocampal_volume < 2500:
                risk += 0.20  # Severe atrophy
            elif hippocampal_volume < 2800:
                risk += 0.10  # Moderate atrophy

        # Ensure risk is bounded
        risk_score = max(0.01, min(risk, 0.90))

        # === Risk category and recommendation ===
        if risk_score < 0.3:
            risk_category = "low"
            recommendation = (
                "Low risk. Maintain healthy lifestyle (exercise, Mediterranean diet, cognitive engagement). "
                "Routine cognitive screening every 1–2 years."
            )
        elif risk_score < 0.6:
            risk_category = "moderate"
            recommendation = (
                "Moderate risk. Consider neuropsychological evaluation and vascular risk management "
                "(hypertension, diabetes, cholesterol). Discuss biomarker testing (e.g., amyloid PET) if indicated."
            )
        else:
            risk_category = "high"
            recommendation = (
                "High risk. Urgent referral to memory disorders clinic or neurologist. "
                "Comprehensive evaluation (MRI, CSF biomarkers, cognitive testing) recommended."
            )

        # Log successful prediction
        log_usage(
            function_name="calculate_risk_score",
            metadata=input_data,
            result={
                "risk_score": risk_score,
                "risk_category": risk_category,
                "recommendation": recommendation,
            },
        )

        return AlzheimerRiskScreenerOutput(
            patient_id=input_schema.patient_id,
            risk_score=risk_score,
            risk_category=risk_category,
            recommendation=recommendation,
            model_name="rule_based_risk_v1",
        )

    except Exception as e:
        # Fallback on error: do not penalize missing data harshly
        try:
            log_usage(
                function_name="calculate_risk_score_error",
                metadata=input_data,
                result={"error": str(e)},
            )
        except Exception:
            pass  # silent fail on logging error

        return AlzheimerRiskScreenerOutput(
            patient_id=input_schema.patient_id,
            risk_score=0.0,
            risk_category="error",
            recommendation="An error occurred during risk assessment.",
            model_name="rule_based_risk_v1",
            error=str(e),
        )
    
__all__ = ["calculate_risk_score"]