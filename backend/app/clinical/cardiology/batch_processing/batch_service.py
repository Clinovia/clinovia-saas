# backend/app/clinical/cardiology/batch_processing/batch_service.py
import csv
import io
from typing import List, Dict, Any, Callable, Type
from uuid import uuid4

from pydantic import BaseModel
from supabase import create_client, Client

# ---------------------------------------------------------------------
# Supabase client
# ---------------------------------------------------------------------
SUPABASE_URL = "https://<your-project>.supabase.co"
SUPABASE_KEY = "<service_role_or_anon_key>"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------------------------------------------------------------------
# Generic batch processing (Supabase-only)
# ---------------------------------------------------------------------
def run_batch(
    *,
    file_bytes: bytes,
    clinician_id: str,
    input_schema_cls: Type[BaseModel],
    model_function: Callable,
    assessment_type: str,  # e.g., "CARDIOLOGY_ASCVD"
    specialty: str,
    model_name: str,
    model_version: str,
    use_cache: bool = True,
    supabase_table: str = "assessments",
) -> List[Dict[str, Any]]:
    """
    Generic batch execution engine for clinical assessments (Supabase-only).

    - Parses CSV input
    - Converts rows into Pydantic input schemas
    - Runs the model function per row
    - Saves results directly to Supabase
    - Isolates failures to individual rows
    """
    rows = _parse_csv(file_bytes)
    results: List[Dict[str, Any]] = []

    for index, row in enumerate(rows):
        try:
            input_schema = input_schema_cls(**row)

            # Run model function directly
            model_output = model_function(input_schema)

            # Wrap in Pydantic schema if applicable
            output = (
                input_schema_cls(**model_output) if isinstance(model_output, dict) else model_output
            )

            # Prepare Supabase record
            result_record = {
                "clinician_id": clinician_id,
                "patient_id": row.get("patient_id") or str(uuid4()),
                "assessment_type": assessment_type,
                "specialty": specialty,
                "model_name": model_name,
                "model_version": model_version,
                "status": "completed",
                "result": output.model_dump() if hasattr(output, "model_dump") else dict(output),
            }

            # Save result to Supabase
            supabase.table(supabase_table).insert(result_record).execute()

            results.append({
                "row": index + 1,
                "patient_id": row.get("patient_id"),
                "status": "completed",
                "result": result_record["result"]
            })

        except Exception as e:
            error_record = {
                "clinician_id": clinician_id,
                "patient_id": row.get("patient_id") or str(uuid4()),
                "assessment_type": assessment_type,
                "specialty": specialty,
                "model_name": model_name,
                "model_version": model_version,
                "status": "failed",
                "error": str(e),
            }

            # Save errors to Supabase
            supabase.table(supabase_table).insert(error_record).execute()

            results.append({
                "row": index + 1,
                "patient_id": row.get("patient_id"),
                "status": "failed",
                "error": str(e)
            })

    return results


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def _parse_csv(file_bytes: bytes) -> List[Dict[str, Any]]:
    """
    Decode CSV bytes and return a list of normalized row dictionaries.
    """
    decoded = file_bytes.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))
    rows = list(reader)
    if not rows:
        raise ValueError("Uploaded CSV file is empty")
    return [_normalize_row(row) for row in rows]


def _normalize_row(row: Dict[str, str]) -> Dict[str, Any]:
    """
    Normalize CSV row values:
    - empty → None
    - numeric strings → float
    - otherwise → stripped string
    """
    normalized: Dict[str, Any] = {}
    for key, value in row.items():
        if value is None or value.strip() == "":
            normalized[key] = None
            continue
        try:
            normalized[key] = float(value)
        except ValueError:
            normalized[key] = value.strip()
    return normalized
