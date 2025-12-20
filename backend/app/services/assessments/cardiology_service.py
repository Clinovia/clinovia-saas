from typing import Optional
from uuid import UUID

from app.services.patients.patient_service import PatientService
from app.schemas.cardiology import (
    ASCVDRiskInput,
    CHA2DS2VAScInput,
    BPCategoryInput,
    ECGInterpretationInput,
    EchonetEFInput,
)
from app.services.cardiology import (
    ascvd_service,
    bp_service,
    cha2ds2vasc_service,
    ecg_service,
    ef_service,
)
from app.services.assessment_pipeline import run_assessment_pipeline
from app.db.models.assessments import AssessmentType
from app.db.repositories.assessment_repository import AssessmentRepository


class CardiologyAssessmentService:
    """Orchestrates all cardiology assessment workflows."""

    def __init__(
        self,
        patient_service: PatientService,
        clinician_id: UUID,
        db_session,
    ):
        self.patient_service = patient_service
        self.clinician_id = clinician_id
        self.db = db_session

        self.ascvd = ascvd_service
        self.cha2ds2vasc = cha2ds2vasc_service
        self.bp = bp_service
        self.ecg = ecg_service
        self.ef = ef_service

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def _get_patient_or_raise(self, patient_id: Optional[UUID]):
        """Validate patient existence if patient_id is provided."""
        if patient_id is None:
            return None

        patient = self.patient_service.get(patient_id, self.clinician_id)
        if not patient:
            raise ValueError("Patient not found or unauthorized")

        return patient

    # ------------------------------------------------------------------
    # Individual Assessments (pipeline-based)
    # ------------------------------------------------------------------

    def run_ascvd(self, patient_id: Optional[UUID], input_schema: ASCVDRiskInput) -> dict:
        self._get_patient_or_raise(patient_id)

        result = run_assessment_pipeline(
            input_schema=input_schema,
            db=self.db,
            clinician_id=self.clinician_id,
            patient_id=patient_id,
            model_function=self.ascvd.run_ascvd_prediction,
            assessment_type=AssessmentType.CARDIOLOGY_ASCVD,
            specialty="cardiology",
            model_name="ascvd",
        )
        return result.model_dump(mode="json")

    def run_cha2ds2vasc(self, patient_id: Optional[UUID], input_schema: CHA2DS2VAScInput) -> dict:
        self._get_patient_or_raise(patient_id)

        result = run_assessment_pipeline(
            input_schema=input_schema,
            db=self.db,
            clinician_id=self.clinician_id,
            patient_id=patient_id,
            model_function=self.cha2ds2vasc.run_cha2ds2vasc_prediction,
            assessment_type=AssessmentType.CARDIOLOGY_CHA2DS2VASC,
            specialty="cardiology",
            model_name="cha2ds2vasc",
        )
        return result.model_dump(mode="json")

    def run_bp(self, patient_id: Optional[UUID], input_schema: BPCategoryInput) -> dict:
        self._get_patient_or_raise(patient_id)

        result = run_assessment_pipeline(
            input_schema=input_schema,
            db=self.db,
            clinician_id=self.clinician_id,
            patient_id=patient_id,
            model_function=self.bp.run_bp_category_prediction,
            assessment_type=AssessmentType.CARDIOLOGY_BP,
            specialty="cardiology",
            model_name="bp_category",
        )
        return result.model_dump(mode="json")

    def run_ecg(self, patient_id: Optional[UUID], input_schema: ECGInterpretationInput) -> dict:
        self._get_patient_or_raise(patient_id)

        result = run_assessment_pipeline(
            input_schema=input_schema,
            db=self.db,
            clinician_id=self.clinician_id,
            patient_id=patient_id,
            model_function=self.ecg.run_ecg_interpretation,
            assessment_type=AssessmentType.CARDIOLOGY_ECG,
            specialty="cardiology",
            model_name="ecg_interpretation",
        )
        return result.model_dump(mode="json")

    # ------------------------------------------------------------------
    # Ejection Fraction (INTENTIONALLY NOT pipeline-based)
    # ------------------------------------------------------------------

    async def run_ef(self, patient_id: Optional[UUID], input_schema: EchonetEFInput) -> dict:
        """EF uses an external microservice and does NOT go through the pipeline."""
        self._get_patient_or_raise(patient_id)

        result_dict = await self.ef.predict_ejection_fraction(video_file=input_schema.video_file)

        # Persist via standard AssessmentRepository
        AssessmentRepository(self.db).create(
            assessment_type=AssessmentType.CARDIOLOGY_EJECTION_FRACTION,
            clinician_id=self.clinician_id,
            patient_id=patient_id,
            input_data=input_schema.model_dump(mode="json"),
            result=result_dict,
            algorithm_version=result_dict.get("model_version", "1.0.0"),
            status="completed",
        )

        return {**result_dict, "patient_id": patient_id}

    # ------------------------------------------------------------------
    # Combined Assessment
    # ------------------------------------------------------------------

    async def run_full_assessment(
        self,
        patient_id: Optional[UUID],
        ascvd_input: ASCVDRiskInput,
        cha2ds2vasc_input: CHA2DS2VAScInput,
        bp_input: BPCategoryInput,
        ecg_input: ECGInterpretationInput,
        ef_input: EchonetEFInput,
    ) -> dict:
        """Run all cardiology assessments together (patient_id optional)."""
        self._get_patient_or_raise(patient_id)

        return {
            "patient_id": patient_id,
            "ascvd": self.run_ascvd(patient_id, ascvd_input),
            "cha2ds2vasc": self.run_cha2ds2vasc(patient_id, cha2ds2vasc_input),
            "bp_category": self.run_bp(patient_id, bp_input),
            "ecg_result": self.run_ecg(patient_id, ecg_input),
            "ef_result": await self.run_ef(patient_id, ef_input),
        }
