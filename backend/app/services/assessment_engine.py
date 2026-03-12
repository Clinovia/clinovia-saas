from typing import Any, Dict

from app.services.registry import get_assessment_config
from app.repositories.assessments_repository import AssessmentsRepository
from app.services.pdf_engine.assessment_pdf import generate_assessment_pdf
from app.core.supabase_client import supabase


class AssessmentEngine:

    def __init__(self) -> None:
        self.repo = AssessmentsRepository(supabase)

    def run_assessment(
        self,
        *,
        assessment_type: str,
        clinician_id: str,
        patient_id: str,
        input_data: Dict[str, Any],
    ) -> Dict[str, Any]:

        # --------------------------------------------------
        # 1. Load registry configuration
        # --------------------------------------------------

        config = get_assessment_config(assessment_type)

        predict_fn = config["predict_fn"]
        input_schema = config["input_schema"]
        output_schema = config["output_schema"]
        specialty = config["specialty"]

        # --------------------------------------------------
        # 2. Validate input
        # --------------------------------------------------

        validated_input = input_schema(
            patient_id=patient_id,
            **input_data,
        )

        # --------------------------------------------------
        # 3. Run prediction
        # --------------------------------------------------

        prediction_result = predict_fn(validated_input)

        output_data = self._normalize_output(prediction_result)

        # --------------------------------------------------
        # 4. Store assessment
        # --------------------------------------------------

        record = {
            "clinician_id": clinician_id,
            "patient_id": patient_id,
            "assessment_type": assessment_type,
            "specialty": specialty,
            "model_name": output_data.get("model_name"),
            "model_version": output_data.get("model_version"),
            "status": "completed",
            "input_data": input_data,
            "output_data": output_data,
        }

        assessment = self.repo.create(record)

        assessment_id = assessment["id"]

        # --------------------------------------------------
        # 5. Generate PDF
        # --------------------------------------------------

        pdf_path = generate_assessment_pdf(
            assessment=assessment,
            input_schema=input_schema,
            output_schema=output_schema,
            filename=f"/tmp/{assessment_id}.pdf",
        )

        # --------------------------------------------------
        # 6. Upload PDF + update record
        # --------------------------------------------------

        pdf_url = self.repo.upload_pdf(assessment_id, pdf_path)

        self.repo.update_pdf_url(assessment_id, pdf_url)

        return {
            "assessment_id": assessment_id,
            "output": output_data,
            "pdf_url": pdf_url,
        }

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------

    def _normalize_output(self, result: Any) -> Dict[str, Any]:

        if result is None:
            return {}

        if hasattr(result, "model_dump"):
            return result.model_dump(mode="json")

        if hasattr(result, "dict"):
            return result.dict()

        if isinstance(result, dict):
            return result

        try:
            return dict(result)
        except Exception:
            return {"result": result}