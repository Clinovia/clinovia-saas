# app/services/cardiology/cardio_batch_service.py

from fastapi import BackgroundTasks, UploadFile
from typing import List, Dict, Any
from uuid import uuid4
import csv
import io

from app.schemas.cardiology.cardiology import ASCVDInput, ASCVDRiskOutput
from app.clinical.cardiology.ascvd import calculate_ascvd_risk

from supabase import create_client, Client

# ---------------------------------------------------------------------
# Lazy Supabase client
# ---------------------------------------------------------------------
def get_supabase_client():
    """
    Returns a Supabase client if credentials exist in the environment.
    Raises RuntimeError if not set.
    """
    from supabase import create_client, Client

    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError(
            "Supabase credentials not set. Set SUPABASE_URL and SUPABASE_KEY in the environment."
        )

    return create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------------------------------------------------------------------
# Cardiology Batch Service (Supabase-only)
# ---------------------------------------------------------------------
class CardioBatchService:
    """
    Service-level orchestrator for Cardiology ASCVDRisk batch jobs.
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
                        input_data = ASCVDInput(**row)

                        # Run clinical model
                        output_data: ASCVDRiskOutput = ASCVDRiskOutput(**calculate_ascvd_risk(input_data))

                        # Prepare record for Supabase
                        record = {
                            "clinician_id": clinician_id,
                            "patient_id": row.get("patient_id") or str(uuid4()),
                            "assessment_type": "CARDIOLOGY_ASCVD",  # replaced Enum with string
                            "specialty": "cardiology",
                            "model_name": "cardio-ascvd-v1",
                            "model_version": "1.0.0",
                            "status": "completed",
                            "result": output_data.model_dump() if hasattr(output_data, "model_dump") else dict(output_data),
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
