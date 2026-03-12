"""
Rule-based Alzheimer's Risk Screener
------------------------------------
Performs rule-based scoring and risk categorization using clinical factors.
Refactored for schema-based registry integration.
"""

from app.schemas.alzheimer.risk_screener import (
    AlzheimerRiskScreenerInput,
    AlzheimerRiskScreenerOutput,
)

from app.clinical.utils import log_usage
from app.services.registry import register_assessment


def calculate_risk_score(
    input_schema: AlzheimerRiskScreenerInput,
) -> AlzheimerRiskScreenerOutput:

    input_data = input_schema.dict()

    try:
        age = input_data["age"]
        gender = input_data["gender"]
        education_years = input_data["education_years"]
        apoe4_status = input_data["apoe4_status"]
        memory_score = input_data["memory_score"]
        hippocampal_volume = input_data.get("hippocampal_volume")

        risk = 0.03

        if age >= 80:
            risk += 0.40
        elif age >= 75:
            risk += 0.30
        elif age >= 70:
            risk += 0.20
        elif age >= 65:
            risk += 0.10

        if apoe4_status:
            risk += 0.25

        if gender == "female":
            risk += 0.05

        if education_years < 8:
            risk += 0.15
        elif education_years < 12:
            risk += 0.08
        elif education_years >= 16:
            risk -= 0.05

        if memory_score <= 18:
            risk += 0.25
        elif memory_score <= 22:
            risk += 0.15
        elif memory_score <= 25:
            risk += 0.05

        if hippocampal_volume is not None:
            if hippocampal_volume < 2500:
                risk += 0.20
            elif hippocampal_volume < 2800:
                risk += 0.10

        risk_score = max(0.01, min(risk, 0.90))

        if risk_score < 0.3:
            category = "low"
            recommendation = (
                "Low risk. Maintain healthy lifestyle and routine screening."
            )
        elif risk_score < 0.6:
            category = "moderate"
            recommendation = (
                "Moderate risk. Consider neuropsychological evaluation and risk factor management."
            )
        else:
            category = "high"
            recommendation = (
                "High risk. Referral to neurologist or memory disorders clinic recommended."
            )

        result = AlzheimerRiskScreenerOutput(
            patient_id=input_schema.patient_id,
            risk_score=risk_score,
            risk_category=category,
            recommendation=recommendation,
            model_name="rule_based_risk_v1",
        )

        log_usage(
            function_name="alzheimer_risk_screener",
            metadata=input_data,
            result=result.dict(),
        )

        return result

    except Exception as e:

        log_usage(
            function_name="alzheimer_risk_screener_error",
            metadata=input_data,
            result={"error": str(e)},
        )

        return AlzheimerRiskScreenerOutput(
            patient_id=input_schema.patient_id,
            risk_score=0.0,
            risk_category="error",
            recommendation="An error occurred during risk assessment.",
            model_name="rule_based_risk_v1",
            error=str(e),
        )


# ===============================
# Registry Registration
# ===============================

register_assessment(
    name="alzheimer_risk_screener",
    input_schema=AlzheimerRiskScreenerInput,
    output_schema=AlzheimerRiskScreenerOutput,
    runner=calculate_risk_score,
)