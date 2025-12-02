"""
Utility functions for clinical AI modules
-----------------------------------------
Includes model loading, preprocessing, logging, helper functions, and video conversion.
"""

import os
import uuid
import joblib
import pandas as pd
import numpy as np
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, List, Tuple
import tempfile
from functools import lru_cache

import torch
import boto3

from app.clinical.cardiology.models.ef3dcnn_model import EF3DCNN

# -----------------------------
# S3 client / bucket config
# -----------------------------
S3_BUCKET = os.environ.get("CLINOVIA_S3_BUCKET", "clinovia.ai")
_s3_client = boto3.client("s3")


# ============================================================
# Gender Encoding
# ============================================================
def encode_gender(gender: Optional[str]) -> int:
    """
    Encode gender as integer:
      - 0 = male
      - 1 = female
      - 2 = unknown / other
    """
    if gender is None:
        return 2

    gender = gender.lower()
    if gender in ("male", "m"):
        return 0
    elif gender in ("female", "f"):
        return 1
    return 2


# ============================================================
# Default Filling
# ============================================================
def fill_defaults(input_dict: dict, numeric_defaults: dict, categorical_defaults: dict) -> dict:
    """
    Fill missing numeric and categorical fields with defaults.
    """
    filled = input_dict.copy()

    # Numeric fields
    for key, default_value in numeric_defaults.items():
        if key not in filled or filled[key] is None:
            filled[key] = default_value

    # Categorical fields
    for key, default_value in categorical_defaults.items():
        if key not in filled or filled[key] is None:
            filled[key] = default_value

    return filled


# ============================================================
# Preprocessing helpers
# ============================================================
def preprocess_for_prediction_dataframe(
    input_data: Dict[str, Any],
    numeric_defaults: Dict[str, Any],
    categorical_defaults: Dict[str, Any],
    feature_order: List[str],
    numeric_columns: List[str],
    categorical_columns: List[str],
    scaler: Optional[Any] = None,
) -> pd.DataFrame:
    """Preprocess input data and return as DataFrame with proper feature names."""
    data_filled = fill_defaults(input_data, numeric_defaults, categorical_defaults)
    
    for cat_col in categorical_columns:
        if cat_col == "PTGENDER" and cat_col in data_filled:
            data_filled[cat_col] = encode_gender(data_filled[cat_col])
    
    try:
        numeric_values = [data_filled[col] for col in numeric_columns]
    except KeyError as e:
        raise KeyError(f"Missing required numeric feature after defaults: {e}")
    
    if scaler:
        numeric_df = pd.DataFrame([numeric_values], columns=numeric_columns)
        numeric_scaled = scaler.transform(numeric_df)
        numeric_scaled_dict = dict(zip(numeric_columns, numeric_scaled[0]))
    else:
        numeric_scaled_dict = dict(zip(numeric_columns, numeric_values))

    try:
        categorical_values = [data_filled[col] for col in categorical_columns]
    except KeyError as e:
        raise KeyError(f"Missing required categorical feature after defaults: {e}")
    
    categorical_dict = dict(zip(categorical_columns, categorical_values))
    feature_dict = {**numeric_scaled_dict, **categorical_dict}
    
    try:
        X_df = pd.DataFrame([feature_dict], columns=feature_order)
    except KeyError as e:
        raise ValueError(
            f"Feature '{e.args[0]}' in feature_order not found in processed features. "
            f"Available: {list(feature_dict.keys())}"
        )
    
    return X_df


def preprocess_for_prediction(
    input_data: Dict[str, Any],
    numeric_defaults: Dict[str, Any],
    categorical_defaults: Dict[str, Any],
    feature_order: List[str],
    numeric_columns: List[str],
    categorical_columns: List[str],
    scaler: Optional[Any] = None,
) -> np.ndarray:
    """Preprocess input data and return as numpy array."""
    data_filled = fill_defaults(input_data, numeric_defaults, categorical_defaults)
    
    for cat_col in categorical_columns:
        if cat_col == "PTGENDER" and cat_col in data_filled:
            data_filled[cat_col] = encode_gender(data_filled[cat_col])
    
    try:
        numeric_values = [data_filled[col] for col in numeric_columns]
    except KeyError as e:
        raise KeyError(f"Missing required numeric feature after defaults: {e}")
    
    if scaler:
        numeric_array = np.array(numeric_values, dtype=float).reshape(1, -1)
        numeric_scaled = scaler.transform(numeric_array).flatten()
    else:
        numeric_scaled = np.array(numeric_values, dtype=float).flatten()
    
    try:
        categorical_values = [data_filled[col] for col in categorical_columns]
    except KeyError as e:
        raise KeyError(f"Missing required categorical feature after defaults: {e}")
    
    feature_dict = {}
    for col, val in zip(numeric_columns, numeric_scaled):
        feature_dict[col] = val
    for col, val in zip(categorical_columns, categorical_values):
        feature_dict[col] = val
    
    try:
        X = np.array([feature_dict[f] for f in feature_order], dtype=float).reshape(1, -1)
    except KeyError as e:
        raise ValueError(
            f"Feature '{e.args[0]}' in feature_order not found in processed features. "
            f"Available: {list(feature_dict.keys())}"
        )
    
    if X.shape[1] != len(feature_order):
        raise ValueError(
            f"Output shape mismatch: expected {len(feature_order)} features, "
            f"got {X.shape[1]}. Check feature_order vs numeric/categorical columns."
        )
    
    return X


def build_df_from_order(order: Dict[str, Any], columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Build DataFrame from dictionary with optional column ordering."""
    df = pd.DataFrame([order])
    if columns:
        df = df.reindex(columns=columns)
    return df


# ============================================================
# Video Conversion
# ============================================================
def convert_to_mp4(input_path: str) -> str:
    """Convert video to MP4 format using FFmpeg."""
    input_path = Path(input_path)
    output_path = Path(f"/tmp/{uuid.uuid4().hex}.mp4")

    command = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output_path),
    ]

    try:
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg conversion failed: {e.stderr.decode()}")

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise RuntimeError("FFmpeg conversion produced an empty file.")

    return str(output_path)


# ============================================================
# MODEL LOADING FROM S3
# ============================================================
@lru_cache(maxsize=32)
def _download_s3_to_tempfile(bucket: str, key: str) -> str:
    """
    Download S3 object to a temporary file and return the local path.
    Results are cached by (bucket, key) to avoid redundant downloads.
    """
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=Path(key).suffix)
    tmp.close()
    _s3_client.download_file(Bucket=bucket, Key=key, Filename=tmp.name)
    return tmp.name


def load_model(
    model_key: str, 
    preprocessor_key: Optional[str] = None
) -> Tuple[Any, Optional[Any]]:
    """
    Download and load sklearn/joblib model and optional preprocessor from S3.
    
    All models are stored in s3://clinovia.ai/
    
    Args:
        model_key: S3 key to model file (e.g., "models/alzheimer/diagnosis_screening/v1/model.joblib")
        preprocessor_key: Optional S3 key to preprocessor (e.g., scaler)
    
    Returns:
        Tuple of (model, preprocessor)
    
    Example:
        model, scaler = load_model(
            "models/alzheimer/diagnosis_screening/v1/model.joblib",
            "models/alzheimer/diagnosis_screening/v1/scaler.joblib"
        )
    """
    if not S3_BUCKET:
        raise ValueError(
            "S3_BUCKET not configured. Set CLINOVIA_S3_BUCKET environment variable."
        )
    
    print(f"📥 Loading model from S3: s3://{S3_BUCKET}/{model_key}")
    
    model_path = _download_s3_to_tempfile(S3_BUCKET, model_key)
    try:
        model = joblib.load(model_path)
    except Exception as e:
        try:
            os.remove(model_path)
        except Exception:
            pass
        raise RuntimeError(f"Failed to load model from S3: {e}") from e
    
    preprocessor = None
    if preprocessor_key:
        print(f"📥 Loading preprocessor from S3: s3://{S3_BUCKET}/{preprocessor_key}")
        pre_path = _download_s3_to_tempfile(S3_BUCKET, preprocessor_key)
        try:
            preprocessor = joblib.load(pre_path)
        except Exception as e:
            try:
                os.remove(pre_path)
            except Exception:
                pass
            raise RuntimeError(f"Failed to load preprocessor from S3: {e}") from e
    
    return model, preprocessor


# ============================================================
# PYTORCH MODEL LOADING (EF CNN)
# ============================================================
def load_ef_model(model_key: str, device: str = "cpu"):
    """
    Load EF3DCNN PyTorch model from S3.
    
    Args:
        model_key: S3 key to model file (e.g., "models/cardiology/ef/v1/ef3dcnn_epoch17.pth")
        device: "cpu" or "cuda"
    
    Returns:
        Loaded and initialized EF3DCNN model in eval mode
    """
    if not S3_BUCKET:
        raise ValueError(
            "S3_BUCKET not configured. Set CLINOVIA_S3_BUCKET environment variable."
        )
    
    print(f"📥 Loading EF model from S3: s3://{S3_BUCKET}/{model_key}")
    
    model = EF3DCNN()
    
    # Download to temp file
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pth")
    tmp_file.close()
    
    try:
        _s3_client.download_file(Bucket=S3_BUCKET, Key=model_key, Filename=tmp_file.name)
        state_dict = torch.load(tmp_file.name, map_location=device, weights_only=True)
        model.load_state_dict(state_dict)
    except Exception as e:
        raise RuntimeError(f"Failed to load EF model from S3: {e}") from e
    finally:
        # Clean up temp file
        try:
            os.remove(tmp_file.name)
        except Exception:
            pass
    
    model.to(device)
    model.eval()
    return model


def is_model_loaded(model: Optional[torch.nn.Module]) -> bool:
    """Check if a PyTorch model is initialized and in eval mode."""
    return (
        model is not None
        and isinstance(model, torch.nn.Module)
        and not model.training
    )


# ============================================================
# LOGGING
# ============================================================
def log_usage(function_name: str, metadata: dict | None = None, result: dict | None = None):
    """Simple, uniform usage logging."""
    print(f"[{function_name}] METADATA: {metadata} | RESULT: {result}")


# ============================================================
# EXPORTS
# ============================================================
__all__ = [
    "encode_gender",
    "fill_defaults",
    "preprocess_for_prediction",
    "preprocess_for_prediction_dataframe",
    "build_df_from_order",
    "load_model",
    "load_ef_model",
    "is_model_loaded",
    "log_usage",
    "convert_to_mp4",
]