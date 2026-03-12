from uuid import uuid4, UUID
import os
from typing import Optional

from supabase import create_client, Client

from app.schemas.alzheimer.prognosis_2yr_extended import (
    AlzheimerPrognosis2yrExtendedInput,
    AlzheimerPrognosis2yrExtendedOutput,
)
from app.clinical.alzheimer.ml_models.prognosis_2yr_extended import (
    predict_prognosis_2yr_extended,
)

_supabase_client: Optional[Client] = None


# ---------------------------------------------------------
# Cached Supabase client
# ---------------------------------------------------------
def get_supabase_client() -> Client:
    global _supabase_client

    if _supabase_client:
        return _supabase_client

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError("Supabase credentials not set.")

    _supabase_client = create_client(url, key)
    return _supabase_client


# ---------------------------------------------------------
# UUID Validation
# ---------------------------------------------------------
def validate_uuid(value: str, field_name: str) -> str:
    try:
        return str(UUID(value))
    except Exception:
        raise RuntimeError(f"Invalid UUID for {field_name}: {value}")


# ---------------------------------------------------------
# Alzheimer 2-Year Prognosis (Extended)
# ---------------------------------------------------------
def run_prognosis_2yr_extended(
    *,
    input_schema: AlzheimerPrognosis2yrExtendedInput,
    clinician_id: str,
    patient_id: Optional[str] = None,
    supabase_table: str = "assessments",
) -> AlzheimerPrognosis2yrExtendedOutput:

    # ✅ Validate UUIDs FIRST
    clinician_uuid = validate_uuid(clinician_id, "clinician_id")

    if patient_id:
        patient_uuid = validate_uuid(patient_id, "patient_id")
    else:
        patient_uuid = str(uuid4())

    # Ensure Pydantic input
    input_data = (
        input_schema
        if isinstance(input_schema, AlzheimerPrognosis2yrExtendedInput)
        else AlzheimerPrognosis2yrExtendedInput(**input_schema)
    )

    # Run ML model
    output: AlzheimerPrognosis2yrExtendedOutput = predict_prognosis_2yr_extended(
        input_data
    )

    # Standardized Supabase record
    record = {
        "clinician_id": clinician_uuid,
        "patient_id": patient_uuid,
        "assessment_type": "ALZHEIMER_PROGNOSIS_2YR_EXTENDED",
        "specialty": "alzheimer",
        "model_name": output.model_name,
        "model_version": output.model_version,
        "status": "completed",
        "input_data": input_data.model_dump(mode="json"),
        "output_data": output.model_dump(mode="json"),
    }

    # Insert safely
    supabase = get_supabase_client()
    response = supabase.table(supabase_table).insert(record).execute()

    if hasattr(response, "error") and response.error:
        raise RuntimeError(response.error)

    if not getattr(response, "data", None):
        raise RuntimeError("Insert succeeded but returned no data.")

    return output