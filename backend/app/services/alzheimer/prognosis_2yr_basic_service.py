from uuid import uuid4, UUID
import os
from typing import Optional

from supabase import create_client, Client

from app.schemas.alzheimer.prognosis_2yr_basic import (
    AlzheimerPrognosis2yrBasicInput,
    AlzheimerPrognosis2yrBasicOutput,
)
from app.clinical.alzheimer.ml_models.prognosis_2yr_basic import (
    predict_prognosis_2yr_basic,
)

_supabase_client: Optional[Client] = None


# ---------------------------------------------------------
# Cached Supabase client (same pattern as screening)
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
# UUID Validation (prevents DB crashes)
# ---------------------------------------------------------
def validate_uuid(value: str, field_name: str) -> str:
    try:
        return str(UUID(value))
    except Exception:
        raise RuntimeError(f"Invalid UUID for {field_name}: {value}")


# ---------------------------------------------------------
# Alzheimer 2-Year Prognosis (Basic)
# ---------------------------------------------------------
def run_prognosis_2yr_basic(
    *,
    input_schema: AlzheimerPrognosis2yrBasicInput,
    clinician_id: str,
    patient_id: Optional[str] = None,
    supabase_table: str = "assessments",
) -> AlzheimerPrognosis2yrBasicOutput:

    # ✅ Validate UUIDs FIRST (critical)
    clinician_uuid = validate_uuid(clinician_id, "clinician_id")

    if patient_id:
        patient_uuid = validate_uuid(patient_id, "patient_id")
    else:
        patient_uuid = str(uuid4())

    # Ensure Pydantic input
    input_data = (
        input_schema
        if isinstance(input_schema, AlzheimerPrognosis2yrBasicInput)
        else AlzheimerPrognosis2yrBasicInput(**input_schema)
    )

    # Run ML model
    output: AlzheimerPrognosis2yrBasicOutput = predict_prognosis_2yr_basic(input_data)

    # Standardized Supabase record
    record = {
        "clinician_id": clinician_uuid,
        "patient_id": patient_uuid,
        "assessment_type": "ALZHEIMER_PROGNOSIS_2YR_BASIC",
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

    # Explicit DB error handling (same pattern as screening)
    if hasattr(response, "error") and response.error:
        raise RuntimeError(response.error)

    if not getattr(response, "data", None):
        raise RuntimeError("Insert succeeded but returned no data.")

    return output