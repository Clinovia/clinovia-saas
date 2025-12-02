from pathlib import Path
from typing import Optional, Union
from uuid import uuid4
import tempfile
import logging
import numpy as np
import cv2
import torch
import torchvision.transforms as T

from app.clinical.utils import load_ef_model, convert_to_mp4
from app.schemas.cardiology import EchonetEFInput, EchonetEFOutput
from app.schemas.common import PredictionStatus  # ← Import PredictionStatus

logger = logging.getLogger(__name__)

# -----------------------------
# Configuration
# -----------------------------
S3_MODEL_KEY = "models/cardiology/ejection-fraction/v1/ef3dcnn_epoch17.pth"
BUCKET_NAME = "clinovia.ai"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DEFAULT_TARGET_SIZE = (112, 112)
DEFAULT_MAX_FRAMES = 32

# Clinical thresholds (ASE/EACVI)
EF_THRESHOLDS = {"normal": 50, "mild": 40, "moderate": 30}


# -----------------------------
# Video I/O
# -----------------------------
def _read_video_frames(video_path: str, max_frames: int = DEFAULT_MAX_FRAMES) -> torch.Tensor:
    """Read video frames using OpenCV and return as [T, H, W, C] tensor."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")

    frames = []
    while len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame_rgb)
    cap.release()

    if not frames:
        raise ValueError("No frames extracted from video")

    video = torch.from_numpy(np.array(frames, dtype=np.uint8))

    # Pad or sample to fixed length
    if len(video) < max_frames:
        last_frame = video[-1].unsqueeze(0)
        video = torch.cat([video, last_frame.repeat(max_frames - len(video), 1, 1, 1)], dim=0)
    elif len(video) > max_frames:
        indices = torch.linspace(0, len(video) - 1, max_frames).long()
        video = video[indices]

    return video


# -----------------------------
# Video preprocessing
# -----------------------------
def _preprocess_video(video_path: str, target_size: tuple = DEFAULT_TARGET_SIZE, max_frames: int = DEFAULT_MAX_FRAMES) -> torch.Tensor:
    """Convert video to mp4, load, and preprocess into model-ready tensor [1, C, T, H, W]."""
    try:
        video_path = convert_to_mp4(video_path)
        video = _read_video_frames(video_path, max_frames=max_frames)
    except Exception as e:
        logger.error(f"Video read failed: {e}")
        raise ValueError(f"Failed to read video: {e}") from e

    video = video.float() / 255.0  # normalize to [0,1]

    # Convert to grayscale if needed
    if video.shape[-1] == 3:
        grayscale = 0.299 * video[:, :, :, 0] + 0.587 * video[:, :, :, 1] + 0.114 * video[:, :, :, 2]
        video = grayscale.unsqueeze(-1)
    elif video.shape[-1] != 1:
        raise ValueError(f"Unsupported channel count: {video.shape[-1]}. Expected 1 or 3.")

    # Resize frames
    video = video.permute(0, 3, 1, 2)  # [T, C, H, W]
    video = T.Resize(target_size)(video)

    # Add batch dimension and permute to [batch, channels, frames, H, W]
    video = video.unsqueeze(0).permute(0, 2, 1, 3, 4)
    return video


# -----------------------------
# Clinical categorization
# -----------------------------
def _categorize_ef(ef_percent: float) -> str:
    """Categorize EF based on ASE/EACVI thresholds."""
    if ef_percent >= EF_THRESHOLDS["normal"]:
        return "Normal"
    elif ef_percent >= EF_THRESHOLDS["mild"]:
        return "Mild"
    elif ef_percent >= EF_THRESHOLDS["moderate"]:
        return "Moderate"
    else:
        return "Severe"


# -----------------------------
# Public API
# -----------------------------
def predict_ejection_fraction_from_bytes(video_bytes: bytes, patient_id: Optional[Union[str, int]] = None, filename: str = "video.mp4") -> EchonetEFOutput:
    """
    Predict ejection fraction from video bytes.
    """
    patient_id = patient_id or "N/A"
    prediction_id = str(uuid4())
    temp_path = None

    try:
        if not video_bytes:
            raise ValueError("Empty video data")

        # Save video bytes to temp file
        suffix = Path(filename).suffix or '.mp4'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(video_bytes)
            temp_path = tmp.name

        logger.info(f"Saved {len(video_bytes)} bytes to temp file: {temp_path}")

        # Preprocess video
        video_tensor = _preprocess_video(temp_path)

        # Load model from S3
        model = load_ef_model(S3_MODEL_KEY, device=DEVICE)
        model.eval()

        with torch.no_grad():
            ef_pred = model(video_tensor.to(DEVICE)).item()

        ef_pred = max(0.0, min(100.0, ef_pred))
        ef_pred = round(float(ef_pred), 2)
        category = _categorize_ef(ef_pred)

        warnings = []
        if ef_pred < 30:
            warnings.append("Severely reduced ejection fraction - urgent cardiology evaluation recommended")
        elif ef_pred < 40:
            warnings.append("Moderately reduced ejection fraction - consider cardiology referral")

        logger.info(f"Prediction successful: EF={ef_pred}%, category={category}")

        return EchonetEFOutput(
            ef_percent=ef_pred,
            category=category,
            model_name="echonet_3dcnn",
            model_version="1.0.0",
            prediction_id=prediction_id,
            status=PredictionStatus.SUCCESS,
            confidence=None,
            warnings=warnings or None,
            error=None
        )

    except Exception as e:
        logger.exception(f"EF prediction failed for patient {patient_id}")
        return EchonetEFOutput(
            patient_id=patient_id,
            ef_percent=None,
            category="Error",
            model_name="echonet_3dcnn",
            model_version="1.0.0",
            prediction_id=prediction_id,
            status=PredictionStatus.ERROR,
            confidence=None,
            warnings=None,
            error=str(e)
        )

    finally:
        # Clean up temp file
        if temp_path and Path(temp_path).exists():
            try:
                Path(temp_path).unlink()
                logger.debug(f"Cleaned up temp file: {temp_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up temp file {temp_path}: {e}")


# -----------------------------
# Legacy support
# -----------------------------
def predict_ejection_fraction_from_path(video_path: str, patient_id: Optional[Union[str, int]] = None) -> EchonetEFOutput:
    with open(video_path, 'rb') as f:
        video_bytes = f.read()
    return predict_ejection_fraction_from_bytes(video_bytes, patient_id, filename=Path(video_path).name)


def predict_ejection_fraction(input_data: EchonetEFInput) -> EchonetEFOutput:
    return predict_ejection_fraction_from_path(input_data.video_file, input_data.patient_id)


# Expose public API
__all__ = [
    "predict_ejection_fraction_from_bytes",
    "predict_ejection_fraction_from_path",
    "predict_ejection_fraction",
]
