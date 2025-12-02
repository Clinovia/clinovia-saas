# backend/app/clinical/alzheimer/ml_models/diagnosis_extended.py
"""
Extended Alzheimer's diagnosis classifier (CN, MCI, AD).
Uses pre-trained model with numeric and categorical preprocessing.
Includes cognitive, demographic, imaging, and biomarker features.
"""

from typing import Any, Dict
from uuid import uuid4
import numpy as np

from app.schemas.alzheimer.diagnosis_extended import (
    AlzheimerDiagnosisExtendedInput,
    AlzheimerDiagnosisExtendedOutput,
)
from app.clinical.utils import (
    encode_gender,
    fill_defaults,
    preprocess_for_prediction,
    load_model,
    log_usage,
)

# -----------------------------
# Constants
# -----------------------------

CLASS_NAMES = ["CN", "MCI", "AD"]

EXTENDED_FEATURE_ORDER = [
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
    "Hippocampus_bl",
    "Ventricles_bl",
    "WholeBrain_bl",
    "Entorhinal_bl",
    "FDG_bl",
    "AV45_bl",
    "PIB_bl",
    "FBB_bl",
    "ABETA_bl",
    "TAU_bl",
    "PTAU_bl",
    "mPACCdigit_bl",
    "mPACCtrailsB_bl",
]

NUMERIC_COLUMNS = [c for c in EXTENDED_FEATURE_ORDER if c not in ("PTGENDER", "APOE4")]
CATEGORICAL_COLUMNS = ["PTGENDER", "APOE4"]

MODEL_PATH = "models/alzheimer/diagnosis_extended/v1/diagnosis_extended_model.pkl"
PREPROCESSOR_PATH = "models/alzheimer/diagnosis_extended/v1/diagnosis_extended_scaler.pkl"

# Default values to handle missing data gracefully
NUMERIC_DEFAULTS = {
    "AGE": 75,
    "MMSE_bl": 28,
    "CDRSB_bl": 0.5,
    "FAQ_bl": 0.0,
    "PTEDUCAT": 16,
    "RAVLT_immediate_bl": 40.0,
    "MOCA_bl": 26.0,
    "ADAS13_bl": 10.5,
    "Hippocampus_bl": 3500.0,
    "Ventricles_bl": 40000.0,
    "WholeBrain_bl": 1.0e6,
    "Entorhinal_bl": 3000.0,
    "FDG_bl": 1.1,
    "AV45_bl": 1.0,
    "PIB_bl": 1.0,
    "FBB_bl": 1.0,
    "ABETA_bl": 800.0,
    "TAU_bl": 250.0,
    "PTAU_bl": 25.0,
    "mPACCdigit_bl": 0.0,
    "mPACCtrailsB_bl": 0.0,
}

CATEGORICAL_DEFAULTS = {
    "PTGENDER": "female",
    "APOE4": -1,
}


def predict_cognitive_status_extended(
    input_schema: AlzheimerDiagnosisExtendedInput,
) -> AlzheimerDiagnosisExtendedOutput:
    """
    Public API entrypoint for Alzheimer's extended classifier.

    Predicts cognitive status (CN, MCI, or AD) using comprehensive data including
    demographics, cognitive tests, brain imaging, and CSF biomarkers.
    """
    try:
        # Convert input to dict
        input_data = input_schema.model_dump()
        print("DEBUG: input_data =", input_data)

        # Load model and preprocessor
        model, preprocessor = load_model(
            model_key=MODEL_PATH,
            preprocessor_key=PREPROCESSOR_PATH,
        )
        print("DEBUG: model loaded?", model is not None, "preprocessor loaded?", preprocessor is not None)

        # Fill missing defaults and encode categorical features
        input_filled = fill_defaults(input_data, NUMERIC_DEFAULTS, CATEGORICAL_DEFAULTS)
        print("DEBUG: input_filled =", input_filled)

        # Preprocess for model (scaling, ordering)
        X_scaled = preprocess_for_prediction(
            input_data=input_filled,
            numeric_defaults={},  # Already filled
            categorical_defaults={},  # Already filled
            feature_order=EXTENDED_FEATURE_ORDER,
            numeric_columns=NUMERIC_COLUMNS,
            categorical_columns=CATEGORICAL_COLUMNS,
            scaler=preprocessor,
        )
        print("DEBUG: X_scaled =", X_scaled)

        # Make prediction
        y_proba = model.predict_proba(X_scaled)[0]
        print("DEBUG: raw model probabilities =", y_proba)

        y_pred_idx = int(np.argmax(y_proba))
        predicted_class = CLASS_NAMES[y_pred_idx]
        print("DEBUG: predicted_class =", predicted_class)

        probabilities = {cls: float(prob) for cls, prob in zip(CLASS_NAMES, y_proba)}
        confidence = float(np.max(y_proba))

        # Log usage
        log_usage(
            function_name="predict_cognitive_status_extended",
            metadata={k: input_filled[k] for k in EXTENDED_FEATURE_ORDER},
            result={
                "predicted_class": predicted_class,
                "confidence": confidence,
                "probabilities": probabilities,
            },
        )

        # Return output schema
        return AlzheimerDiagnosisExtendedOutput(
            patient_id=input_schema.patient_id,
            predicted_class=predicted_class,
            confidence=confidence,
            probabilities=probabilities,
            prediction_id=str(uuid4()),
            model_version="1.0.0",
        )

    except Exception as e:
        print("DEBUG: exception occurred:", e)
        log_usage("predict_cognitive_status_extended_error", {}, {"error": str(e)})
        return AlzheimerDiagnosisExtendedOutput(
            patient_id=input_schema.patient_id,
            predicted_class=None,
            confidence=0.0,
            probabilities={},
            prediction_id=str(uuid4()),
            model_version="1.0.0",
            error=str(e),
        )