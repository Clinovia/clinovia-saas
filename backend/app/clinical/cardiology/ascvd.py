# app/clinical/cardiology/ascvd_risk.py

"""
ASCVD 10-Year Risk Calculator
-----------------------------
Implements the 2013 ACC/AHA Pooled Cohort Equations (PCE)
for estimating 10-year atherosclerotic cardiovascular disease (ASCVD) risk.

Refactored for schema-based consistency and clinical safety.
"""
from uuid import uuid4
import math
from typing import Dict, Any

from app.schemas.cardiology import ASCVDRiskInput, ASCVDRiskOutput
from app.clinical.utils import log_usage
from app.clinical.cardiology.ascvd_coefficients import _PCE_CONSTANTS


# ==========================================================
# Internal helpers
# ==========================================================
def _validate_input(data: Dict[str, Any]) -> None:
    """Validate physiological and demographic ranges per PCE guidelines."""
    if not (40 <= data["age"] <= 79):
        raise ValueError("Age must be between 40 and 79.")
    if data["gender"].lower() not in {"male", "female"}:
        raise ValueError("Gender must be 'male' or 'female'.")
    if data["race"].lower() not in {"white", "black", "hispanic", "asian", "other"}:
        raise ValueError("Race must be one of: white, black, hispanic, asian, other.")
    if not (130 <= data["total_cholesterol"] <= 320):
        raise ValueError("Total cholesterol must be between 130 and 320 mg/dL.")
    if not (20 <= data["hdl_cholesterol"] <= 100):
        raise ValueError("HDL cholesterol must be between 20 and 100 mg/dL.")
    if not (90 <= data["systolic_bp"] <= 200):
        raise ValueError("Systolic BP must be between 90 and 200 mmHg.")


def _compute_terms(data: Dict[str, Any]) -> Dict[str, float]:
    """Compute base logarithmic and indicator variables."""
    ln_age = math.log(data["age"])
    return {
        "ln_age": ln_age,
        "ln_age_sq": ln_age * ln_age,
        "ln_tc": math.log(data["total_cholesterol"]),
        "ln_hdl": math.log(data["hdl_cholesterol"]),
        "ln_sbp": math.log(data["systolic_bp"]),
        "trt": 1 if data["on_hypertension_treatment"] else 0,
        "smoker": 1 if data["smoker"] else 0,
        "diabetes": 1 if data["diabetes"] else 0,
    }


def _build_feature_terms(data: Dict[str, Any], gender: str, race: str) -> Dict[str, float]:
    """Construct feature terms per PCE specification by gender and race."""
    base = _compute_terms(data)
    terms = {
        "ln_age": base["ln_age"],
        "ln_tc": base["ln_tc"],
        "ln_hdl": base["ln_hdl"],
        "smoker": base["smoker"],
        "diabetes": base["diabetes"],
    }

    # Add age-squared and interaction terms for non-Black males and all females
    if not (gender == "male" and race == "black"):
        terms.update({
            "ln_age_sq": base["ln_age_sq"],
            "ln_age*ln_tc": base["ln_age"] * base["ln_tc"],
            "ln_age*ln_hdl": base["ln_age"] * base["ln_hdl"],
            "ln_age*smoker": base["ln_age"] * base["smoker"],
        })

    # Add BP terms (treated vs untreated) and age*SBP interactions for Black females
    if base["trt"]:
        terms["ln_sbp_trt"] = base["ln_sbp"]
        if gender == "female" and race == "black":
            terms["ln_age*ln_sbp_trt"] = base["ln_age"] * base["ln_sbp"]
    else:
        terms["ln_sbp_untrt"] = base["ln_sbp"]
        if gender == "female" and race == "black":
            terms["ln_age*ln_sbp_untrt"] = base["ln_age"] * base["ln_sbp"]

    return terms


def _compute_risk(S0: float, mean_lp: float, betas: Dict[str, float], terms: Dict[str, float]) -> float:
    """Compute 10-year ASCVD risk from linear predictor."""
    lp = sum(betas[k] * terms[k] for k in terms if k in betas)
    deviation = lp - mean_lp

    # Prevent overflow in exp()
    if deviation > 709:
        survival = 0.0
    elif deviation < -709:
        survival = 1.0
    else:
        survival = S0 ** math.exp(deviation)

    risk = 1.0 - survival
    return max(0.0, min(1.0, risk))


def _categorize_risk(risk_pct: float) -> str:
    """Categorize ASCVD risk per clinical guidelines."""
    if risk_pct >= 20:
        return "high"
    elif risk_pct >= 7.5:
        return "intermediate"
    elif risk_pct >= 5:
        return "borderline"
    else:
        return "low"


# ==========================================================
# Public API (Schema I/O)
# ==========================================================
def calculate_ascvd(input_data: ASCVDRiskInput) -> ASCVDRiskOutput:
    """
    Calculate 10-year ASCVD risk using 2013 ACC/AHA Pooled Cohort Equations.

    input_data: Pydantic model ASCVDRiskInput
    """
    # Convert to dict internally for calculations
    data: Dict[str, Any] = input_data.dict()

    try:
        _validate_input(data)

        gender = data["gender"].lower()
        cohort_race = "black" if data["race"].lower() == "black" else "white"

        params = _PCE_CONSTANTS.get((gender, cohort_race))
        if params is None:
            raise ValueError(f"Unsupported combination: gender={gender}, race={cohort_race}")

        terms = _build_feature_terms(data, gender, cohort_race)
        risk = _compute_risk(params.S0, params.mean_lp, params.betas, terms)
        risk_pct = round(risk * 100, 2)
        category = _categorize_risk(risk_pct)

        log_usage(
            function_name="predict_ascvd_risk_score",
            metadata=data,  # previous 'inputs'
            result={"risk_percentage": risk_pct, "risk_category": category},  # previous 'outputs'
        )

        return ASCVDRiskOutput(
            patient_id=data.get("patient_id"),
            risk_percentage=risk_pct,
            risk_category=category,
            prediction_id=str(uuid4()),
            model_version="v1.0",
        )

    except Exception as e:
        log_usage(
            function_name="predict_ascvd_risk_score_error",
            inputs=data,
            outputs={"error": str(e)},
        )

        return ASCVDRiskOutput(
            patient_id=data.get("patient_id"),
            risk_percentage=0.0,
            risk_category="low",
            prediction_id=str(uuid4()),
            model_version="v1.0",
        )


__all__ = ["calculate_ascvd"]
