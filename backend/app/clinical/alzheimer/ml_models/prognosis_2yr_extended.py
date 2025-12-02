# app/clinical/alzheimer/ml_models/prognosis_2yr_extended.py

"""
Extended Alzheimer's 2-year progression predictor (Stable vs. Progress).
Uses pre-trained model with CSF biomarkers (ABETA, TAU, PTAU).
"""

from typing import Any, Dict
import numpy as np

from app.schemas.alzheimer.prognosis_2yr_extended import (
    AlzheimerPrognosis2yrExtendedInput,
    AlzheimerPrognosis2yrExtendedOutput,
)
from app.clinical.utils import (
    fill_defaults,
    preprocess_for_prediction,
    load_model,
    log_usage,
)

# -----------------------------
# Constants (FROM ACTUAL TRAINED MODEL)
# -----------------------------
CLASS_NAMES = ["Stable", "Progress"]

# Exact feature configuration from trained model
NUMERIC_COLUMNS = ['AGE', 'PTEDUCAT', 'ADAS13', 'CDRSB', 'FAQ', 'GDTOTAL', 'ABETA', 'TAU', 'PTAU']
CATEGORICAL_COLUMNS = ['PTGENDER', 'APOE4_count']
PROGRESS_EXTENDED_FEATURE_ORDER = ['AGE', 'PTGENDER', 'PTEDUCAT', 'ADAS13', 'CDRSB', 'FAQ', 'APOE4_count', 'GDTOTAL', 'ABETA', 'TAU', 'PTAU']

MODEL_PATH = "models/alzheimer/prognosis_2yr_extended/v1/prognosis_2yr_extended_model.pkl"
PREPROCESSOR_PATH = "models/alzheimer/prognosis_2yr_extended/v1/prognosis_2yr_extended_scaler.pkl"

# Domain-informed defaults for missing values
NUMERIC_DEFAULTS = {
    "AGE": 75,
    "PTEDUCAT": 16,
    "ADAS13": 10.5,
    "CDRSB": 0.5,
    "FAQ": 0.0,
    "GDTOTAL": 5.0,
    # CSF biomarker defaults (typical values for MCI patients)
    "ABETA": 700.0,  # pg/mL (lower = more pathology)
    "TAU": 300.0,    # pg/mL (higher = more pathology)
    "PTAU": 50.0,    # pg/mL (higher = more pathology)
}

CATEGORICAL_DEFAULTS = {
    "PTGENDER": "female",
    "APOE4_count": 0,
}


# -----------------------------
# Public API function (Schema I/O)
# -----------------------------
def predict_prognosis_2yr_extended(
    input_schema: AlzheimerPrognosis2yrExtendedInput,
) -> AlzheimerPrognosis2yrExtendedOutput:
    """
    Predict 2-year Alzheimer's progression (Stable vs. Progress).
    Returns expressive probabilities and risk level.
    """

    input_data: Dict[str, Any] = input_schema.model_dump()

    try:
        # -----------------------------
        # Load model + preprocessor
        # -----------------------------
        model, preprocessor = load_model(
            model_key=MODEL_PATH,
            preprocessor_key=PREPROCESSOR_PATH,
        )

        # -----------------------------
        # Fill missing values
        # -----------------------------
        input_filled = fill_defaults(
            input_data,
            NUMERIC_DEFAULTS,
            CATEGORICAL_DEFAULTS
        )

        # -----------------------------
        # Preprocess features
        # -----------------------------
        X_scaled = preprocess_for_prediction(
            input_data=input_filled,
            numeric_defaults=NUMERIC_DEFAULTS,
            categorical_defaults=CATEGORICAL_DEFAULTS,
            feature_order=PROGRESS_EXTENDED_FEATURE_ORDER,
            numeric_columns=NUMERIC_COLUMNS,
            categorical_columns=CATEGORICAL_COLUMNS,
            scaler=preprocessor,
        )

        # -----------------------------
        # Predict
        # -----------------------------
        y_proba = model.predict_proba(X_scaled)[0]
        probabilities = {
            cls: float(prob) for cls, prob in zip(CLASS_NAMES, y_proba)
        }

        prob_stable = float(probabilities["Stable"])
        prob_progress = float(probabilities["Progress"])

        # -----------------------------
        # Risk level determination
        # -----------------------------
        if prob_progress < 0.20:
            risk_level = "low"
        elif prob_progress < 0.50:
            risk_level = "moderate"
        else:
            risk_level = "high"

        # -----------------------------
        # Natural language explanation
        # -----------------------------
        summary_text = (
            f"The patient has a {risk_level} ({prob_progress * 100:.1f}%) "
            f"probability of progressing to Alzheimer's dementia within 2 years."
        )

        # Basic model feature example (placeholder)
        top_features = ["CDRSB", "ADAS13", "AGE"]

        # -----------------------------
        # Logging
        # -----------------------------
        log_usage(
            function_name="predict_progression_extended",
            metadata={k: input_filled[k] for k in PROGRESS_EXTENDED_FEATURE_ORDER},
            result={
                "probability_progression_to_AD_within_2yrs": prob_progress,
                "probability_stable_within_2yrs": prob_stable,
                "risk_level": risk_level,
            },
        )

        # -----------------------------
        # Return expressive output schema
        # -----------------------------
        return AlzheimerPrognosis2yrExtendedOutput(
            patient_id=input_schema.patient_id,
            model_name="prognosis_2yr_extended_v1",
            probability_progression_to_AD_within_2yrs=prob_progress,
            probability_stable_within_2yrs=prob_stable,
            risk_level=risk_level,
            summary_text=summary_text,
            top_features=top_features,
        )

    except Exception as e:
        log_usage(
            "predict_prognosis_2yr_extended_error",
            {},
            {"error": str(e)}
        )

        return AlzheimerPrognosis2yrExtendedOutput(
            patient_id=input_schema.patient_id,
            model_name="prognosis_2yr_basic_v1",
            probability_progression_to_AD_within_2yrs=None,
            probability_stable_within_2yrs=None,
            risk_level="unknown",
            summary_text="Prediction failed due to an internal error.",
            top_features=None,
            error=str(e),
        )
