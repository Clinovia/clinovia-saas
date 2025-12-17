"""
Utility functions for clinical AI modules
-----------------------------------------
Includes model loading (local-first), preprocessing,
logging, helper functions, and video conversion.
"""

from __future__ import annotations

import os
import uuid
import subprocess
import joblib
import tempfile
from pathlib import Path
from functools import lru_cache
from typing import Any, Dict, Optional, List, Tuple

import numpy as np
import pandas as pd
import torch

# ============================================================
# GLOBAL CONFIG
# ============================================================

MODEL_ROOT = Path(
    os.environ.get("CLINOVIA_MODEL_ROOT", "/opt/clinovia/models")
).resolve()

if not MODEL_ROOT.exists():
    raise RuntimeError(f"MODEL_ROOT does not exist: {MODEL_ROOT}")

# ============================================================
# GENDER ENCODING
# ============================================================

def encode_gender(gender: Optional[str]) -> int:
    """
    Encode gender as integer:
      - 0 = male
      - 1 = female
      - 2 = unknown / other
    """
    if not gender:
        return 2

    gender = gender.lower()
    if gender in ("male", "m"):
        return 0
    if gender in ("female", "f"):
        return 1
    return 2


# ============================================================
# DEFAULT FILLING
# ============================================================

def fill_defaults(
    input_dict: Dict[str, Any],
    numeric_defaults: Dict[str, Any],
    categorical_defaults: Dict[str, Any],
) -> Dict[str, Any]:
    """Fill missing numeric and categorical fields with defaults."""
    filled = dict(input_dict)

    for key, default in numeric_defaults.items():
        if filled.get(key) is None:
            filled[key] = default

    for key, default in categorical_defaults.items():
        if filled.get(key) is None:
            filled[key] = default

    return filled


# ============================================================
# PREPROCESSING HELPERS
# ============================================================

def _encode_categoricals(
    data: Dict[str, Any],
    categorical_columns: List[str],
) -> None:
    """In-place categorical encoding."""
    for col in categorical_columns:
        if col == "PTGENDER" and col in data:
            data[col] = encode_gender(data[col])


def preprocess_for_prediction_dataframe(
    input_data: Dict[str, Any],
    numeric_defaults: Dict[str, Any],
    categorical_defaults: Dict[str, Any],
    feature_order: List[str],
    numeric_columns: List[str],
    categorical_columns: List[str],
    scaler: Optional[Any] = None,
) -> pd.DataFrame:
    """Return preprocessed input as a pandas DataFrame."""
    data = fill_defaults(input_data, numeric_defaults, categorical_defaults)
    _encode_categoricals(data, categorical_columns)

    numeric_df = pd.DataFrame([[data[col] for col in numeric_columns]],
                              columns=numeric_columns)

    if scaler:
        numeric_df[:] = scaler.transform(numeric_df)

    categorical_df = pd.DataFrame([[data[col] for col in categorical_columns]],
                                  columns=categorical_columns)

    X = pd.concat([numeric_df, categorical_df], axis=1)
    return X.reindex(columns=feature_order)


def preprocess_for_prediction(
    input_data: Dict[str, Any],
    numeric_defaults: Dict[str, Any],
    categorical_defaults: Dict[str, Any],
    feature_order: List[str],
    numeric_columns: List[str],
    categorical_columns: List[str],
    scaler: Optional[Any] = None,
) -> np.ndarray:
    """Return preprocessed input as numpy array."""
    df = preprocess_for_prediction_dataframe(
        input_data,
        numeric_defaults,
        categorical_defaults,
        feature_order,
        numeric_columns,
        categorical_columns,
        scaler,
    )

    X = df.to_numpy(dtype=float)
    if X.shape[1] != len(feature_order):
        raise ValueError(
            f"Feature mismatch: expected {len(feature_order)}, got {X.shape[1]}"
        )
    return X


def build_df_from_order(
    order: Dict[str, Any],
    columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    df = pd.DataFrame([order])
    return df.reindex(columns=columns) if columns else df


# ============================================================
# VIDEO CONVERSION
# ============================================================

def convert_to_mp4(input_path: str) -> str:
    """Convert video to MP4 using FFmpeg."""
    input_path = Path(input_path)
    output_path = Path("/tmp") / f"{uuid.uuid4().hex}.mp4"

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
        subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg failed: {e.stderr.decode()}")

    if not output_path.exists() or output_path.stat().st_size == 0:
        raise RuntimeError("FFmpeg produced empty output")

    return str(output_path)


# ============================================================
# MODEL LOADING (LOCAL-FIRST, NO S3)
# ============================================================

@lru_cache(maxsize=32)
def _load_joblib(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")
    return joblib.load(path)


def load_model(
    model_rel_path: str,
    preprocessor_rel_path: Optional[str] = None,
) -> Tuple[Any, Optional[Any]]:
    """
    Load model and optional preprocessor from local disk.

    Paths are relative to MODEL_ROOT.

    Example:
        load_model(
            "alzheimer/diagnosis/basic/v1/model.pkl",
            "alzheimer/diagnosis/basic/v1/scaler.pkl"
        )
    """
    model_path = MODEL_ROOT / model_rel_path
    print(f"📦 Loading model: {model_path}")
    model = _load_joblib(model_path)

    preprocessor = None
    if preprocessor_rel_path:
        pre_path = MODEL_ROOT / preprocessor_rel_path
        print(f"📦 Loading preprocessor: {pre_path}")
        preprocessor = _load_joblib(pre_path)

    return model, preprocessor


def is_model_loaded(model: Optional[torch.nn.Module]) -> bool:
    """Check if PyTorch model is initialized and in eval mode."""
    return (
        model is not None
        and isinstance(model, torch.nn.Module)
        and not model.training
    )


# ============================================================
# LOGGING
# ============================================================

def log_usage(
    function_name: str,
    metadata: Optional[dict] = None,
    result: Optional[dict] = None,
) -> None:
    print(
        f"[{function_name}] "
        f"METADATA={metadata or {}} "
        f"RESULT={result or {}}"
    )


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
    "is_model_loaded",
    "log_usage",
]
