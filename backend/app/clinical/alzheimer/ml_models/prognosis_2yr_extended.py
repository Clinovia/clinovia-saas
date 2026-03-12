"""
Extended Alzheimer's 2-year progression predictor (Stable vs. Progress)
----------------------------------------------------------------------
Predicts probability of progression to AD within 2 years using:
- Clinical assessments
- Genetic marker (APOE4)
- CSF biomarkers (ABETA, TAU, PTAU)
"""

import numpy as np

from app.services.registry import register_assessment

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

ASSESSMENT_TYPE = "ALZHEIMER_PROGNOSIS_2YR_EXTENDED"

CLASS_NAMES = ["Stable", "Progress"]

FEATURE_ORDER = [
    "AGE",
    "PTGENDER",
    "PTEDUCAT",
    "ADAS13",
    "CDRSB",
    "FAQ",
    "APOE4_count",
    "GDTOTAL",
    "ABETA",
    "TAU",
    "PTAU",
]

NUMERIC_COLUMNS = [
    "AGE",
    "PTEDUCAT",
    "ADAS13",
    "CDRSB",
    "FAQ",
    "GDTOTAL",
    "ABETA",
    "TAU",
    "PTAU",
]

CATEGORICAL_COLUMNS = [
    "PTGENDER",
    "APOE4_count",
]

MODEL_PATH = "alzheimer/prognosis_2yr_extended/v1/prognosis_2yr_extended_model.pkl"
PREPROCESSOR_PATH = "alzheimer/prognosis_2yr_extended/v1/prognosis_2yr_extended_scaler.pkl"

MODEL_NAME = "Alzheimer_prognosis_2yr_extended-v1"
MODEL_VERSION = "1.0.0"

NUMERIC_DEFAULTS = {
    "AGE": 75,
    "PTEDUCAT": 16,
    "ADAS13": 10.5,
    "CDRSB": 0.5,
    "FAQ": 0.0,
    "GDTOTAL": 5.0,
    "ABETA": 700.0,
    "TAU": 300.0,
    "PTAU": 50.0,
}

CATEGORICAL_DEFAULTS = {
    "PTGENDER": "female",
    "APOE4_count": 0,
}

TOP_FEATURES_PLACEHOLDER = ["CDRSB", "ADAS13", "AGE"]


@register_assessment(
    ASSESSMENT_TYPE,
    specialty="alzheimer",
    input_schema=AlzheimerPrognosis2yrExtendedInput,
)
def predict_prognosis_2yr_extended(
    input_schema: AlzheimerPrognosis2yrExtendedInput,
) -> AlzheimerPrognosis2yrExtendedOutput:

    input_data = input_schema.model_dump()

    try:

        model, preprocessor = load_model(
            MODEL_PATH,
            PREPROCESSOR_PATH,
        )

        input_filled = fill_defaults(
            input_data,
            NUMERIC_DEFAULTS,
            CATEGORICAL_DEFAULTS,
        )

        X_scaled = preprocess_for_prediction(
            input_data=input_filled,
            numeric_defaults=NUMERIC_DEFAULTS,
            categorical_defaults=CATEGORICAL_DEFAULTS,
            feature_order=FEATURE_ORDER,
            numeric_columns=NUMERIC_COLUMNS,
            categorical_columns=CATEGORICAL_COLUMNS,
            scaler=preprocessor,
        )

        y_proba = model.predict_proba(X_scaled)[0]

        probabilities = {
            cls: float(prob)
            for cls, prob in zip(CLASS_NAMES, y_proba)
        }

        prob_stable = probabilities["Stable"]
        prob_progress = probabilities["Progress"]

        if prob_progress < 0.2:
            risk_level = "low"
        elif prob_progress < 0.5:
            risk_level = "moderate"
        else:
            risk_level = "high"

        summary_text = (
            f"The patient has a {risk_level} ({prob_progress*100:.1f}%) "
            "probability of progressing to Alzheimer's dementia within 2 years."
        )

        log_usage(
            function_name="predict_prognosis_2yr_extended",
            metadata={k: input_filled.get(k) for k in FEATURE_ORDER},
            result={"risk_level": risk_level},
        )

        return AlzheimerPrognosis2yrExtendedOutput(
            patient_id=input_schema.patient_id,
            probability_progression_to_AD_within_2yrs=prob_progress,
            probability_stable_within_2yrs=prob_stable,
            risk_level=risk_level,
            summary_text=summary_text,
            top_features=TOP_FEATURES_PLACEHOLDER,
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
        )

    except Exception as e:

        log_usage(
            function_name="predict_prognosis_2yr_extended_error",
            metadata=input_data,
            result={"error": str(e)},
        )

        return AlzheimerPrognosis2yrExtendedOutput(
            patient_id=input_schema.patient_id,
            probability_progression_to_AD_within_2yrs=None,
            probability_stable_within_2yrs=None,
            risk_level="unknown",
            summary_text="Prediction failed due to an internal error.",
            top_features=None,
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
            error=str(e),
        )


__all__ = ["predict_prognosis_2yr_extended"]
