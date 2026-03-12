from typing import Optional
from uuid import uuid4, UUID
import os
import logging

from app.schemas.cardiology.cardiology import ASCVDRiskInput, ASCVDRiskOutput
from app.clinical.cardiology.ascvd import calculate_ascvd

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
# UUID validation helpers
# ---------------------------------------------------------------------
def validate_uuid(value: str, field_name: str) -> str:
    try:
        return str(UUID(value))
    except Exception:
        raise RuntimeError(f"Invalid UUID for {field_name}: {value}")


# ---------------------------------------------------------------------
# ASCVDRisk prediction (Supabase-only)
# ---------------------------------------------------------------------
from app.repositories.assessments_repository import AssessmentsRepository
from app.services.cardiology.reports_service import CardioReportsService


def run_ascvd_prediction(
    *,
    input_schema: ASCVDRiskInput,
    clinician_id: str,
    patient_id: Optional[str] = None,
) -> dict:

    input_data = (
        input_schema
        if isinstance(input_schema, ASCVDRiskInput)
        else ASCVDRiskInput(**input_schema)
    )

    clinician_uuid = validate_uuid(clinician_id, "clinician_id")
    patient_uuid = validate_uuid(patient_id, "patient_id") if patient_id else str(uuid4())

    model_result = calculate_ascvd(input_data)

    output: ASCVDRiskOutput = (
        ASCVDRiskOutput(**model_result)
        if isinstance(model_result, dict)
        else model_result
    )

    assessment_record = {
        "clinician_id": clinician_uuid,
        "patient_id": patient_uuid,
        "assessment_type": "CARDIOLOGY_ASCVD",
        "specialty": "cardiology",
        "model_name": "cardiology-ascvd-v1",
        "model_version": "1.0.0",
        "status": "completed",
        "input_data": input_data.model_dump(mode="json"),
        "output_data": output.model_dump(mode="json"),
    }

    assessments_repo = AssessmentsRepository()
    assessment = assessments_repo.create(assessment_record)

    reports_service = CardioReportsService()
    report = reports_service.create_from_assessment(
        assessment=assessment,
        output=output.model_dump(mode="json"),
    )

    return {
        "assessment_id": assessment["id"],
        "report_id": report["id"],
        "output": output,
    }