from typing import Optional
from uuid import uuid4, UUID
import os
import logging

from app.schemas.cardiology.cardiology import (
    BPCategoryInput,
    BPCategoryOutput,
)
from app.clinical.cardiology.bp_category import categorize_blood_pressure


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Lazy Supabase client
# ---------------------------------------------------------------------
def get_supabase_client():
    from supabase import create_client

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "Supabase credentials not set. Set SUPABASE_URL and SUPABASE_KEY."
        )

    return create_client(supabase_url, supabase_key)


# ---------------------------------------------------------------------
# UUID validation helper (match ASCVD pattern)
# ---------------------------------------------------------------------
def validate_uuid(value: str, field_name: str) -> str:
    try:
        return str(UUID(value))
    except Exception:
        raise RuntimeError(f"Invalid UUID for {field_name}: {value}")


# ---------------------------------------------------------------------
# Blood Pressure Categorization (Supabase-only)
# ---------------------------------------------------------------------
def run_bp_category_prediction(
    *,
    input_schema: BPCategoryInput,
    clinician_id: str,
    patient_id: Optional[str] = None,
    supabase_table: str = "assessments",
) -> BPCategoryOutput:
    """
    Run BP categorization and save result to Supabase
    using standardized assessment schema.
    """

    # Ensure Pydantic input
    input_data = (
        input_schema
        if isinstance(input_schema, BPCategoryInput)
        else BPCategoryInput(**input_schema)
    )

    # Validate UUIDs early (fail fast)
    clinician_uuid = validate_uuid(clinician_id, "clinician_id")

    if patient_id:
        patient_uuid = validate_uuid(patient_id, "patient_id")
    else:
        patient_uuid = str(uuid4())

    logger.info("Clinician UUID: %s", clinician_uuid)
    logger.info("Patient UUID: %s", patient_uuid)

    # Run clinical rule/model
    model_result = categorize_blood_pressure(input_data)

    # Ensure Pydantic output
    output: BPCategoryOutput = (
        BPCategoryOutput(**model_result)
        if isinstance(model_result, dict)
        else model_result
    )

    # Standardized Supabase record
    record = {
        "clinician_id": clinician_uuid,
        "patient_id": patient_uuid,
        "assessment_type": "CARDIOLOGY_BP",
        "specialty": "cardiology",
        "model_name": "cardiology-bp-category-v1",
        "model_version": "1.0.0",
        "status": "completed",
        "input_data": input_data.model_dump(mode="json"),
        "output_data": output.model_dump(mode="json"),
    }

    try:
        supabase = get_supabase_client()

        logger.info("Attempting Supabase insert...")
        response = supabase.table(supabase_table).insert(record).execute()

        logger.info("🔎 Supabase raw response: %s", response)

        # Supabase v2 safe handling
        if hasattr(response, "error") and response.error:
            logger.error("❌ Supabase error object: %s", response.error)
            raise RuntimeError(response.error)

        if not getattr(response, "data", None):
            logger.error("❌ Supabase returned no data.")
            raise RuntimeError("Insert succeeded but returned no data.")

    except Exception as e:
        logger.exception("🔥 Supabase insert failed")
        raise RuntimeError(f"Database insert failed: {str(e)}")

    return output