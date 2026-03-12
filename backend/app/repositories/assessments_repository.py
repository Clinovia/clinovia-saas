# backend/app/repositories/assessments_repository.py
from typing import Any, Dict, List, Optional
from supabase import Client


class AssessmentsRepository:
    """
    Repository for interacting with the assessments table.
    """

    def __init__(self, supabase: Client, table_name: str = "assessments"):
        self.supabase = supabase
        self.table_name = table_name

    # -----------------------------
    # Internal helpers
    # -----------------------------

    def _handle_response(self, response) -> Any:
        """Standardized Supabase error handling."""
        if getattr(response, "error", None):
            raise RuntimeError(response.error)

        if response.data is None:
            raise RuntimeError("Supabase returned no data.")

        return response.data

    # -----------------------------
    # Create
    # -----------------------------

    def create(self, record: Dict[str, Any]) -> Dict[str, Any]:
        response = (
            self.supabase
            .table(self.table_name)
            .insert(record)
            .execute()
        )

        data = self._handle_response(response)
        return data[0]

    # -----------------------------
    # Read by ID (PDF generation)
    # -----------------------------

    def get_assessment_by_id(self, assessment_id: str) -> Optional[Dict[str, Any]]:
        response = (
            self.supabase
            .table(self.table_name)
            .select("*")
            .eq("id", assessment_id)
            .single()
            .execute()
        )

        data = self._handle_response(response)
        return data

    # -----------------------------
    # Read by clinician (dashboard)
    # -----------------------------

    def get_by_clinician(self, clinician_id: str) -> List[Dict[str, Any]]:
        response = (
            self.supabase
            .table(self.table_name)
            .select("*")
            .eq("clinician_id", clinician_id)
            .order("created_at", desc=True)
            .execute()
        )

        data = self._handle_response(response)
        return data

    # -----------------------------
    # Batch insert (for CSV upload)
    # -----------------------------

    def create_many(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        response = (
            self.supabase
            .table(self.table_name)
            .insert(records)
            .execute()
        )

        data = self._handle_response(response)
        return data
    
    # -----------------------------
    # Update PDF URL
    # -----------------------------

    def update_pdf_url(self, assessment_id: str, pdf_url: str) -> Dict[str, Any]:

        response = (
            self.supabase
            .table(self.table_name)
            .update({"pdf_url": pdf_url})
            .eq("id", assessment_id)
            .execute()
        )

        data = self._handle_response(response)
        return data[0]


    # -----------------------------
    # Upload PDF to Supabase Storage
    # -----------------------------

    def upload_pdf(self, assessment_id: str, pdf_path: str) -> str:

        storage_path = f"{assessment_id}.pdf"

        with open(pdf_path, "rb") as f:
            self.supabase.storage.from_("assessment-reports").upload(
                storage_path,
                f,
                {"content-type": "application/pdf"},
            )

        public_url = self.supabase.storage.from_("assessment-reports").get_public_url(storage_path)

        return public_url