"""
Blood Pressure Category Calculator
----------------------------------
Categorizes blood pressure per 2017 ACC/AHA Guidelines.

Categories:
- Normal:               <120/<80
- Elevated:             120–129/<80
- Hypertension Stage 1: 130–139 or 80–89
- Hypertension Stage 2: ≥140 or ≥90
- Hypertensive Crisis:  ≥180 or ≥120
"""

from uuid import uuid4
from app.schemas.cardiology import BPCategoryInput, BPCategoryOutput
from app.clinical.utils import log_usage


def categorize_blood_pressure(input_data: BPCategoryInput) -> BPCategoryOutput:
    try:
        systolic = input_data.systolic_bp
        diastolic = input_data.diastolic_bp

        if systolic is None or diastolic is None:
            raise ValueError("Both systolic and diastolic values are required")

        # ACC/AHA 2017 classification
        if systolic >= 180 or diastolic >= 120:
            category = "hypertensive_crisis"
        elif systolic >= 140 or diastolic >= 90:
            category = "hypertension_stage_2"
        elif 130 <= systolic < 140 or 80 <= diastolic < 90:
            category = "hypertension_stage_1"
        elif 120 <= systolic < 130 and diastolic < 80:
            category = "elevated"
        else:
            category = "normal"

        # Log usage with metadata (consistent with Alzheimer code)
        log_usage(
            function_name="categorize_blood_pressure",
            metadata={
                "patient_id": input_data.patient_id,
                "systolic": systolic,
                "diastolic": diastolic,
                "category": category,
            },
        )

        return BPCategoryOutput(
            patient_id=input_data.patient_id,
            systolic_bp=systolic,
            diastolic_bp=diastolic,
            category=category,
            prediction_id=str(uuid4()),
            model_version="v1.0",
            model_name="bp_category_rule_v1",
        )

    except Exception as e:
        log_usage(
            function_name="categorize_blood_pressure_error",
            metadata={
                "patient_id": input_data.patient_id if input_data else None,
                "systolic": getattr(input_data, "systolic_bp", None),
                "diastolic": getattr(input_data, "diastolic_bp", None),
                "error": str(e),
            },
        )
        return BPCategoryOutput(
            patient_id=input_data.patient_id if input_data else None,
            category="error",
            systolic_bp=getattr(input_data, "systolic_bp", None),
            diastolic_bp=getattr(input_data, "diastolic_bp", None),
            prediction_id=str(uuid4()),
            model_version="v1.0",
            model_name="bp_category_rule_v1",
            error=str(e),
        )


__all__ = ["categorize_blood_pressure"]
