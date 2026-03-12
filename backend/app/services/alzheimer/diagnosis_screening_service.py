from uuid import uuid4, UUID
import os
from typing import Optional

from supabase import create_client, Client

from app.schemas.alzheimer.diagnosis_screening import (
    AlzheimerDiagnosisInput,
    AlzheimerDiagnosisOutput,
)
from app.clinical.alzheimer.ml_models.diagnosis_screening import (
    predict_cognitive_status,
)

_supabase_client: Optional[Client] = None


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


def validate_uuid(value: str, field_name: str) -> str:
    try:
        return str(UUID(value))
    except Exception:
        raise RuntimeError(f"Invalid UUID for {field_name}: {value}")


def run_diagnosis_screen(
    *,
    input_schema: AlzheimerDiagnosisInput,
    clinician_id: str,
    patient_id: Optional[str] = None,
    supabase_table: str = "assessments",
) -> AlzheimerDiagnosisOutput:

    # Validate UUIDs FIRST (same as working service)
    clinician_uuid = validate_uuid(clinician_id, "clinician_id")

    if patient_id:
        patient_uuid = validate_uuid(patient_id, "patient_id")
    else:
        patient_uuid = str(uuid4())

    # Run model
    output: AlzheimerDiagnosisOutput = predict_cognitive_status(input_schema)

    record = {
        "clinician_id": clinician_uuid,
        "patient_id": patient_uuid,
        "assessment_type": "ALZHEIMER_DIAGNOSIS_SCREENING",
        "specialty": "alzheimer",
        "model_name": output.model_name,
        "model_version": output.model_version,
        "status": "completed",
        "input_data": input_schema.model_dump(mode="json"),
        "output_data": output.model_dump(mode="json"),
    }

    supabase = get_supabase_client()
    response = supabase.table(supabase_table).insert(record).execute()

    if hasattr(response, "error") and response.error:
        raise RuntimeError(response.error)

    if not getattr(response, "data", None):
        raise RuntimeError("Insert succeeded but returned no data.")

    return output