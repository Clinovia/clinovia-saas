"""
Basic Alzheimer's diagnosis classifier (CN, MCI, AD)
----------------------------------------------------
Uses pre-trained model with standard scaler.
Aligned with AlzheimerDiagnosisBasicInput schema.

This module performs prediction and self-registers
its assessment configuration in the central registry.
"""

import numpy as np

from app.schemas.alzheimer.diagnosis_basic import (
    AlzheimerDiagnosisBasicInput,
    AlzheimerDiagnosisBasicOutput,
)

from app.services.registry import register_assessment

from app.clinical.utils import (
    fill_defaults,
    preprocess_for_prediction,
    load_model,
    log_usage,
)

# -----------------------------
# Registry Metadata
# -----------------------------

ASSESSMENT_TYPE = "ALZHEIMER_DIAGNOSIS_BASIC"
SPECIALTY = "alzheimer"

MODEL_NAME = "Alzheimer_diagnosis_with_basic_features"
MODEL_VERSION = "1.0.0"

# -----------------------------
# Constants
# -----------------------------

CLASS_NAMES = ["CN", "MCI", "AD"]

BASIC_FEATURE_ORDER = [
    "AGE",
    "MMSE",
    "FAQ",
    "PTEDUCAT",
    "RAVLT_immediate",
    "MOCA",
    "ADAS13",
    "PTGENDER",
    "APOE4",
]

NUMERIC_COLUMNS = [
    "AGE",
    "MMSE",
    "FAQ",
    "PTEDUCAT",
    "RAVLT_immediate",
    "MOCA",
    "ADAS13",
]

CATEGORICAL_COLUMNS = [
    "PTGENDER",
    "APOE4",
]

MODEL_PATH = "alzheimer/diagnosis_basic/v1/diagnosis_basic_model.pkl"
PREPROCESSOR_PATH = "alzheimer/diagnosis_basic/v1/diagnosis_basic_scaler.pkl"

# -----------------------------
# Fallback Defaults
# -----------------------------

NUMERIC_DEFAULTS = {
    "AGE": 75.0,
    "MMSE": 28.0,
    "FAQ": 0.0,
    "PTEDUCAT": 16.0,
    "RAVLT_immediate": 40.0,
    "MOCA": 26.0,
    "ADAS13": 10.5,
}

CATEGORICAL_DEFAULTS = {
    "PTGENDER": "female",
    "APOE4": -1,
}


# -----------------------------
# Prediction Function
# -----------------------------

def predict_cognitive_status_basic(
    input_schema: AlzheimerDiagnosisBasicInput,
) -> AlzheimerDiagnosisBasicOutput:
    """
    Predict cognitive status (CN, MCI, AD).
    """

    input_data = input_schema.model_dump()

    try:

        model, preprocessor = load_model(
            MODEL_PATH,
            PREPROCESSOR_PATH,
        )

        X_scaled = preprocess_for_prediction(
            input_data=input_data,
            numeric_defaults=NUMERIC_DEFAULTS,
            categorical_defaults=CATEGORICAL_DEFAULTS,
            feature_order=BASIC_FEATURE_ORDER,
            numeric_columns=NUMERIC_COLUMNS,
            categorical_columns=CATEGORICAL_COLUMNS,
            scaler=preprocessor,
        )

        y_proba = model.predict_proba(X_scaled)[0]
        y_pred_idx = int(np.argmax(y_proba))

        predicted_class = CLASS_NAMES[y_pred_idx]

        probabilities = {
            cls: float(prob)
            for cls, prob in zip(CLASS_NAMES, y_proba)
        }

        confidence = float(np.max(y_proba))

        filled_data = fill_defaults(
            input_data,
            NUMERIC_DEFAULTS,
            CATEGORICAL_DEFAULTS,
        )

        log_usage(
            function_name="predict_cognitive_status_basic",
            metadata={k: filled_data.get(k) for k in BASIC_FEATURE_ORDER},
            result={
                "predicted_class": predicted_class,
                "confidence": confidence,
                "probabilities": probabilities,
            },
        )

        return AlzheimerDiagnosisBasicOutput(
            patient_id=input_schema.patient_id,
            predicted_class=predicted_class,
            confidence=confidence,
            probabilities=probabilities,
            top_features=None,
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
        )

    except Exception as e:

        log_usage(
            function_name="predict_cognitive_status_basic_error",
            metadata={"patient_id": getattr(input_schema, "patient_id", None)},
            result={"error": str(e)},
        )

        return AlzheimerDiagnosisBasicOutput(
            patient_id=getattr(input_schema, "patient_id", None),
            predicted_class=None,
            confidence=0.0,
            probabilities={},
            top_features=None,
            model_name=MODEL_NAME,
            model_version=MODEL_VERSION,
            error=str(e),
        )


# -----------------------------
# Self Registration
# -----------------------------

register_assessment(
    assessment_type=ASSESSMENT_TYPE,
    specialty=SPECIALTY,
    predict_fn=predict_cognitive_status_basic,
    input_schema=AlzheimerDiagnosisBasicInput,
    output_schema=AlzheimerDiagnosisBasicOutput,
)


__all__ = ["predict_cognitive_status_basic"]