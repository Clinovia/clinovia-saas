# app/clinical/alzheimer/ml_models/diagnosis_screening.py
"""
Model inference logic for Alzheimer's diagnosis (CN, MCI, AD).
Uses pre-trained XGBoost pipeline model (includes preprocessing internally).
"""
from typing import Any, Dict
import numpy as np

from app.clinical.utils import (
    load_model,
    build_df_from_order,
    log_usage,
)
from app.schemas.alzheimer.diagnosis_screening import (
    AlzheimerDiagnosisInput,
    AlzheimerDiagnosisOutput,
)

# -----------------------------
# Constants
# -----------------------------

CLASS_NAMES = ["CN", "MCI", "AD"]

FEATURE_ORDER = [
    "age",
    "education_years",
    "moca_score",
    "adas13_score",
    "cdr_sum",
    "faq_total",
    "gender",
    "race",
]

MODEL_PATH = "alzheimer/diagnosis/screening/v1/model.joblib"


# -----------------------------
# Public API function (Schema I/O)
# -----------------------------

def predict_cognitive_status(input_schema: AlzheimerDiagnosisInput) -> AlzheimerDiagnosisOutput:
    """
    Predict cognitive status (CN, MCI, or AD) using a pre-trained XGBoost model.
    Accepts: validated input via AlzheimerDiagnosisInput schema.
    Returns: structured output via AlzheimerDiagnosisOutput schema.
    """
    input_data = input_schema.dict()
    
    # Keep categorical features as STRINGS for OneHotEncoder
    # The pipeline's OneHotEncoder handles the actual encoding
    input_data["gender"] = str(input_data.get("gender", "female")).lower()
    input_data["race"] = str(input_data.get("race", "1"))
    
    # Validate feature presence
    missing_features = [f for f in FEATURE_ORDER if f not in input_data]
    if missing_features:
        raise ValueError(f"Missing required features: {missing_features}")
    
    # Build DataFrame in expected feature order
    df = build_df_from_order(input_data, FEATURE_ORDER)
    
    # CRITICAL: Ensure categorical columns are strings (not mixed types)
    # This prevents the "ufunc 'isnan' not supported" error in OneHotEncoder
    categorical_cols = ["gender", "race"]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)
    
    print(f"DEBUG: df dtypes before prediction:\n{df.dtypes}")
    print(f"DEBUG: df values:\n{df}")
    
    # Load model and predict
    model, _ = load_model(MODEL_PATH)
   
    try:
        y_proba = model.predict_proba(df)[0]
    except Exception as e:
        print(f"DEBUG: Prediction error: {e}")
        print(f"DEBUG: DataFrame info:")
        print(df.info())
        print(f"DEBUG: DataFrame head:")
        print(df.head())
        raise
    
    # Extract prediction results
    y_pred_idx = int(np.argmax(y_proba))
    predicted_class = CLASS_NAMES[y_pred_idx]
    confidence = float(np.max(y_proba))
    probabilities = {cls: float(prob) for cls, prob in zip(CLASS_NAMES, y_proba)}
    
    # Log usage for monitoring
    log_usage("predict_cognitive_status", input_data, {
        "predicted_class": predicted_class,
        "confidence": confidence,
        "probabilities": probabilities,
    })
    
    return AlzheimerDiagnosisOutput(
        patient_id=input_schema.patient_id,
        predicted_class=predicted_class,
        confidence=confidence,
        probabilities=probabilities,
        model_name="alz_model_v1",
    )


__all__ = ["predict_cognitive_status"]