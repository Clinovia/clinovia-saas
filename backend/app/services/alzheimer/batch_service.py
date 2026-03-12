# app/services/alzheimer/alzheimer_batch_service.py

from fastapi import BackgroundTasks, UploadFile
from typing import List, Dict, Any
from uuid import uuid4
import csv
import io

from app.schemas.alzheimer.diagnosis_basic import AlzheimerDiagnosisBasicInput, dict as model_dict
from app.clinical.alzheimer.ml_models.diagnosis_basic import predict_cognitive_status_basic

from supabase import create_client, Client

# ---------------------------------------------------------------------
# Supabase client
# ---------------------------------------------------------------------
SUPABASE_URL = "https://<your-project>.supabase.co"
SUPABASE_KEY = "<service_role_or_anon_key>"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------------------------------------------------------------------
# Alzheimer Batch Service (Supabase-only)
# ---------------------------------------------------------------------
class AlzheimerBatchService:
    """
    Service-level orchestrator for Alzheimer batch jobs.
    Handles background execution and Supabase persistence.
    """

    def __init__(self):
        self.statuses: dict[str, str] = {}

    async def process_batch(
        self,
        *,
        file: UploadFile,
        clinician_id: str,  # Supabase user ID
        background_tasks: BackgroundTasks,
        supabase_table: str = "assessments",
    ):
        batch_id = str(uuid4())
        self.statuses[batch_id] = "processing"

        async def background_job():
            try:
                file_bytes = await file.read()
                rows = self._parse_csv(file_bytes)
                results: List[Dict[str, Any]] = []

                for index, row in enumerate(rows):
                    try:
                        # Convert row to Pydantic schema
                        input_data = AlzheimerDiagnosisBasicInput(**row)

                        # Run clinical model
                        output_data = predict_cognitive_status_basic(input_data)

                        # Wrap output in dict if necessary
                        if hasattr(output_data, "model_dump"):
                            result_data = output_data.model_dump()
                        elif isinstance(output_data, dict):
                            result_data = output_data
                        else:
                            result_data = model_dict(output_data)

                        # Prepare record for Supabase
                        record = {
                            "clinician_id": clinician_id,
                            "patient_id": row.get("patient_id") or str(uuid4()),
                            "assessment_type": "ALZHEIMER_DIAGNOSIS_BASIC",
                            "specialty": "alzheimer",
                            "model_name": "alz-diagnosis-basic-v1",
                            "model_version": "1.0.0",
                            "status": "completed",
                            "result": result_data,
                        }

                        # Insert into Supabase
                        supabase.table(supabase_table).insert(record).execute()

                        results.append({"row": index + 1, "status": "completed"})
                    except Exception as row_err:
                        results.append({"row": index + 1, "status": "failed", "error": str(row_err)})

                self.statuses[batch_id] = "completed"

            except Exception as e:
                self.statuses[batch_id] = f"failed: {str(e)}"

        background_tasks.add_task(background_job)

        return {"batch_id": batch_id}

    def get_status(self, batch_id: str):
        return {
            "batch_id": batch_id,
            "status": self.statuses.get(batch_id, "not_found"),
        }

    # -----------------------------------------------------------------
    # CSV helpers
    # -----------------------------------------------------------------
    def _parse_csv(self, file_bytes: bytes) -> List[Dict[str, Any]]:
        """
        Decode CSV bytes and return a list of row dictionaries.
        """
        decoded = file_bytes.decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded))
        rows = list(reader)
        if not rows:
            raise ValueError("Uploaded CSV file is empty")
        return [self._normalize_row(row) for row in rows]

    def _normalize_row(self, row: Dict[str, str]) -> Dict[str, Any]:
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
