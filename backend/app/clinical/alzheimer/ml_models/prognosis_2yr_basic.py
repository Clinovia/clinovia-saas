import numpy as np

from app.services.registry import register_assessment

from app.schemas.alzheimer.prognosis_2yr_basic import (
    AlzheimerPrognosis2yrBasicInput,
    AlzheimerPrognosis2yrBasicOutput,
)

from app.clinical.utils import (
    fill_defaults,
    preprocess_for_prediction_dataframe,
    load_model,
    log_usage,
)

ASSESSMENT_TYPE = "ALZHEIMER_PROGNOSIS_2YR_BASIC"

CLASS_NAMES = ["Stable", "Progress"]

FEATURE_ORDER = [
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
    "AGE",
    "PTEDUCAT",
    "ADAS13",
    "MOCA",
    "CDRSB",
    "FAQ",
    "GDTOTAL",
]

CATEGORICAL_COLUMNS = [
    "PTGENDER",
    "APOE4_count",
]

MODEL_PATH = "alzheimer/prognosis_2yr_basic/v1/prognosis_2yr_basic_model.pkl"
PREPROCESSOR_PATH = "alzheimer/prognosis_2yr_basic/v1/prognosis_2yr_basic_scaler.pkl"

MODEL_NAME = "Alzheimer_prognosis_2yr_basic-v1"
MODEL_VERSION = "1.0.0"

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

TOP_FEATURES_PLACEHOLDER = ["CDRSB", "ADAS13", "AGE"]


@register_assessment(
    ASSESSMENT_TYPE,
    specialty="alzheimer",
    input_schema=AlzheimerPrognosis2yrBasicInput,
)
def predict_prognosis_2yr_basic(
    input_schema: AlzheimerPrognosis2yrBasicInput,
) -> AlzheimerPrognosis2yrBasicOutput:

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

        X_scaled = preprocess_for_prediction_dataframe(
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
            function_name="predict_prognosis_2yr_basic",
            metadata={k: input_filled.get(k) for k in FEATURE_ORDER},
            result={"risk_level": risk_level},
        )

        return AlzheimerPrognosis2yrBasicOutput(
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
            function_name="predict_prognosis_2yr_basic_error",
            metadata=input_data,
            result={"error": str(e)},
        )

        return AlzheimerPrognosis2yrBasicOutput(
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