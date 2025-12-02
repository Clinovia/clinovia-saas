"""
Basic ECG interpretation rules for rhythm, intervals, and morphology.
This is a rule-based decision-support component, not a standalone diagnostic tool.
"""

from typing import List, Literal
from uuid import uuid4
from app.schemas.cardiology import ECGInterpretationInput, ECGInterpretationOutput
from app.clinical.utils import log_usage


# ==========================================================
# Input Validation
# ==========================================================
def _validate_ecg_input(data: ECGInterpretationInput) -> None:
    """Validate input ranges and values."""
    if not (20 <= data.heart_rate <= 300):
        raise ValueError("Heart rate must be between 20 and 300 bpm")
    if not (40 <= data.qrs_duration <= 200):
        raise ValueError("QRS duration must be between 40 and 200 ms")
    
    valid_rhythms = {"sinus", "afib", "flutter", "other"}
    if data.rhythm.lower() not in valid_rhythms:
        raise ValueError(f"Rhythm must be one of: {sorted(valid_rhythms)}")
    
    if data.qt_interval is not None and not (200 <= data.qt_interval <= 600):
        raise ValueError("QT interval must be between 200 and 600 ms (if provided)")
    if data.pr_interval is not None and not (80 <= data.pr_interval <= 400):
        raise ValueError("PR interval must be between 80 and 400 ms (if provided)")


# ==========================================================
# Public API
# ==========================================================
def interpret_ecg(data: ECGInterpretationInput) -> ECGInterpretationOutput:
    """
    Interpret ECG parameters and return structured output.

    Args:
        data: ECG parameter input including rhythm, intervals, and morphology

    Returns:
        ECGInterpretationOutput: Interpretation findings, rhythm, risk, and metadata
    """
    try:
        # Validate input
        _validate_ecg_input(data)
        
        findings: List[str] = []
        rhythm = data.rhythm.lower()
        overall_risk: Literal["routine", "urgent", "emergent"] = "routine"

        # PR interval assessment
        if data.pr_interval is not None:
            if data.pr_interval > 200:
                findings.append("first_degree_av_block")
                overall_risk = "urgent" if overall_risk == "routine" else overall_risk
            elif data.pr_interval < 120 and rhythm == "sinus":
                findings.append("short_pr_interval")
                overall_risk = "urgent" if overall_risk == "routine" else overall_risk

        # Rhythm assessment
        if rhythm == "afib":
            findings.append("afib")
            overall_risk = "urgent"
        elif rhythm == "flutter":
            findings.append("atrial_flutter")
            overall_risk = "urgent"

        # Heart rate assessment (for sinus rhythm)
        if rhythm == "sinus":
            if data.heart_rate > 100:
                findings.append("sinus_tachycardia")
            elif data.heart_rate < 60:
                findings.append("sinus_bradycardia")

        # QRS duration assessment
        if data.qrs_duration > 120:
            findings.append("wide_qrs_complex")

        # ST segment and T-wave assessment (critical findings)
        if data.st_elevation:
            findings.append("st_elevation")
            overall_risk = "emergent"
        if data.t_wave_inversion:
            findings.append("t_wave_inversion")
            overall_risk = "urgent" if overall_risk == "routine" else overall_risk

        # QT interval assessment
        if data.qt_interval is not None and data.qt_interval > 450:
            findings.append("prolonged_qt")
            overall_risk = "urgent" if overall_risk == "routine" else overall_risk

        # Default to normal if no abnormalities found
        if not findings:
            findings.append("normal")

        output = ECGInterpretationOutput(
            patient_id=data.patient_id,
            findings=findings,
            rhythm=rhythm,
            overall_risk=overall_risk,
            prediction_id=str(uuid4()),
            model_name="ecg_interpreter_rule_v1",
            model_version="1.0.0"
        )

        # Log usage using metadata style
        log_usage(
            function_name="interpret_ecg",
            metadata={
                "patient_id": data.patient_id,
                "input": data.model_dump(),
                "output": output.model_dump(),
            },
        )

        return output

    except Exception as e:
        log_usage(
            function_name="interpret_ecg_error",
            metadata={
                "patient_id": getattr(data, "patient_id", None),
                "error": str(e),
                "input": data.model_dump() if data else {},
            },
        )
        return ECGInterpretationOutput(
            patient_id=getattr(data, "patient_id", None),
            findings=["error"],
            rhythm="unknown",
            overall_risk="routine",
            prediction_id=str(uuid4()),
            model_name="ecg_interpreter_rule_v1",
            model_version="1.0.0",
            error=str(e)
        )


__all__ = ["interpret_ecg"]
