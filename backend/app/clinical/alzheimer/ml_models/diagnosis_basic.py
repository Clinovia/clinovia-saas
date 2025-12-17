# backend/app/clinical/alzheimer/ml_models/diagnosis_basic.py
"""
Basic Alzheimer's diagnosis classifier (CN, MCI, AD)
----------------------------------------------------
Uses pre-trained model with standard scaler.
Refactored for consistent schema and preprocessing.
"""

from typing import Dict
from uuid import uuid4
import numpy as np

from app.schemas.alzheimer.diagnosis_basic import (
    AlzheimerDiagnosisBasicInput,
    AlzheimerDiagnosisBasicOutput,
)
from app.clinical.utils import (
    fill_defaults,
    preprocess_for_prediction,
    load_model,
    log_usage,
)

# -----------------------------
# Constants
# -----------------------------

CLASS_NAMES = ["CN", "MCI", "AD"]

# Feature order MUST match model training order
BASIC_FEATURE_ORDER = [
    "AGE",
    "MMSE_bl",
    "CDRSB_bl",
    "FAQ_bl",
    "PTEDUCAT",
    "PTGENDER",
    "APOE4",
    "RAVLT_immediate_bl",
    "MOCA_bl",
    "ADAS13_bl",
]

# Numeric features (will be scaled)
NUMERIC_COLUMNS = [
    "AGE",
    "MMSE_bl",
    "CDRSB_bl",
    "FAQ_bl",
    "PTEDUCAT",
    "RAVLT_immediate_bl",
    "MOCA_bl",
    "ADAS13_bl",
]

# Categorical features (will be encoded but not scaled)
CATEGORICAL_COLUMNS = ["PTGENDER", "APOE4"]

MODEL_PATH = "alzheimer/diagnosis/basic/v1/model.pkl"
PREPROCESSOR_PATH = "alzheimer/diagnosis/basic/v1/scaler.pkl"

# Default values for missing numeric fields
NUMERIC_DEFAULTS = {
    "AGE": 75.0,
    "MMSE_bl": 28.0,
    "CDRSB_bl": 0.5,
    "FAQ_bl": 0.0,
    "PTEDUCAT": 16.0,
    "RAVLT_immediate_bl": 40.0,
    "MOCA_bl": 26.0,
    "ADAS13_bl": 10.5,
}

# Default values for missing categorical fields
CATEGORICAL_DEFAULTS = {
    "PTGENDER": "female",
    "APOE4": -1,
}


def predict_cognitive_status_basic(
    input_schema: AlzheimerDiagnosisBasicInput,
) -> AlzheimerDiagnosisBasicOutput:
    """
    Public API entrypoint for Alzheimer's basic classifier.

    Predicts cognitive status (CN, MCI, AD) from cognitive assessment data.
    """
    try:
        input_data = input_schema.model_dump()
        print("DEBUG: input_data =", input_data)

        # Load model and preprocessor
        model, preprocessor = load_model(
            MODEL_PATH,
            PREPROCESSOR_PATH,
        )
        print("DEBUG: model loaded?", model is not None, "preprocessor loaded?", preprocessor is not None)

        # Preprocess using the shared utility
        X_scaled = preprocess_for_prediction(
            input_data=input_data,
            numeric_defaults=NUMERIC_DEFAULTS,
            categorical_defaults=CATEGORICAL_DEFAULTS,
            feature_order=BASIC_FEATURE_ORDER,
            numeric_columns=NUMERIC_COLUMNS,
            categorical_columns=CATEGORICAL_COLUMNS,
            scaler=preprocessor,
        )
        print("DEBUG: X_scaled shape =", X_scaled.shape)
        print("DEBUG: X_scaled =", X_scaled)

        # Make prediction
        y_proba = model.predict_proba(X_scaled)[0]
        print("DEBUG: raw model probabilities =", y_proba)

        y_pred_idx = int(np.argmax(y_proba))
        predicted_class = CLASS_NAMES[y_pred_idx]
        print("DEBUG: predicted_class =", predicted_class)

        probabilities = {cls: float(prob) for cls, prob in zip(CLASS_NAMES, y_proba)}
        confidence = float(np.max(y_proba))

        # Log usage - get actual values used (after defaults applied)
        filled_data = fill_defaults(input_data, NUMERIC_DEFAULTS, CATEGORICAL_DEFAULTS)
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
            prediction_id=str(uuid4()),
            model_version="1.0.0",
        )

    except Exception as e:
        import traceback
        print("DEBUG: exception occurred:", e)
        traceback.print_exc()
        log_usage("predict_cognitive_status_basic_error", {}, {"error": str(e)})
        return AlzheimerDiagnosisBasicOutput(
            patient_id=input_schema.patient_id,
            predicted_class=None,
            confidence=0.0,
            probabilities={},
            prediction_id=str(uuid4()),
            model_version="1.0.0",
            error=str(e),
        )