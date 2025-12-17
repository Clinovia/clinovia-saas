# app/clinical/alzheimer/ml_models/prognosis_2yr_basic.py

"""
Basic Alzheimer's 2-year progression predictor (Stable vs. Progress).
Uses pre-trained RandomForest model with numeric scaling and categorical encoding.
"""

from typing import Any, Dict
import numpy as np

from app.schemas.alzheimer.prognosis_2yr_basic import (
    AlzheimerPrognosis2yrBasicInput,
    AlzheimerPrognosis2yrBasicOutput,
)
from app.clinical.utils import (
    encode_gender,
    fill_defaults,
    preprocess_for_prediction_dataframe,
    load_model,
    log_usage,
)

# -----------------------------
# Constants
# -----------------------------
CLASS_NAMES = ["Stable", "Progress"]

PROGRESS_BASIC_FEATURE_ORDER = [
    "AGE",
    "PTGENDER",
    "PTEDUCAT",
    "ADAS13",
    "MOCA",
    "CDRSB",
    "FAQ",
    "APOE4_count",
    "GDTOTAL",
]

NUMERIC_COLUMNS = [
    "AGE", "PTEDUCAT", "ADAS13", "MOCA", "CDRSB", "FAQ", "GDTOTAL"
]
CATEGORICAL_COLUMNS = ["PTGENDER", "APOE4_count"]

MODEL_PATH = "alzheimer/prognosis/2yr_basic/v1/model.pkl"
PREPROCESSOR_PATH = "alzheimer/prognosis/2yr_basic/v1/scaler.pkl"

NUMERIC_DEFAULTS = {
    "AGE": 75,
    "PTEDUCAT": 16,
    "ADAS13": 10.5,
    "MOCA": 26.0,
    "CDRSB": 0.5,
    "FAQ": 0.0,
    "GDTOTAL": 5.0,
}

CATEGORICAL_DEFAULTS = {
    "PTGENDER": "female",
    "APOE4_count": 0,
}


# -----------------------------
# Public API function (Schema I/O)
# -----------------------------
def predict_prognosis_2yr_basic(
    input_schema: AlzheimerPrognosis2yrBasicInput,
) -> AlzheimerPrognosis2yrBasicOutput:
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
        X_scaled = preprocess_for_prediction_dataframe(
            input_data=input_filled,
            numeric_defaults=NUMERIC_DEFAULTS,
            categorical_defaults=CATEGORICAL_DEFAULTS,
            feature_order=PROGRESS_BASIC_FEATURE_ORDER,
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
            function_name="predict_progression_basic",
            metadata={k: input_filled[k] for k in PROGRESS_BASIC_FEATURE_ORDER},
            result={
                "probability_progression_to_AD_within_2yrs": prob_progress,
                "probability_stable_within_2yrs": prob_stable,
                "risk_level": risk_level,
            },
        )

        # -----------------------------
        # Return expressive output schema
        # -----------------------------
        return AlzheimerPrognosis2yrBasicOutput(
            patient_id=input_schema.patient_id,
            model_name="prognosis_2yr_basic_v1",
            probability_progression_to_AD_within_2yrs=prob_progress,
            probability_stable_within_2yrs=prob_stable,
            risk_level=risk_level,
            summary_text=summary_text,
            top_features=top_features,
        )

    except Exception as e:
        log_usage(
            "predict_prognosis_2yr_basic_error",
            {},
            {"error": str(e)}
        )

        return AlzheimerPrognosis2yrBasicOutput(
            patient_id=input_schema.patient_id,
            model_name="prognosis_2yr_basic_v1",
            probability_progression_to_AD_within_2yrs=None,
            probability_stable_within_2yrs=None,
            risk_level="unknown",
            summary_text="Prediction failed due to an internal error.",
            top_features=None,
            error=str(e),
        )
