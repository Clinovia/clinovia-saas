from typing import Optional
from uuid import UUID
from app.services.patients.patient_service import PatientService
from app.schemas.cardiology import (
    ASCVDRiskInput,
    CHA2DS2VAScInput,
    BPCategoryInput,
    ECGInterpretationInput,
    EFInput,
)
from app.services.cardiology import (
    ascvd_service,
    bp_service,
    cha2ds2vasc_service,
    ecg_service,
    ef_service
)
from app.services.assessment_pipeline import run_assessment_pipeline
from app.db.models.assessments import AssessmentType


class CardiologyAssessmentService:
    """Orchestrates all cardiology assessment workflows."""

    def __init__(self, patient_service: PatientService, clinician_id: UUID, db_session):
        self.patient_service = patient_service
        self.clinician_id = clinician_id
        self.db = db_session
        self.ascvd = ascvd_service
        self.cha2ds2vasc = cha2ds2vasc_service
        self.bp = bp_service
        self.ecg = ecg_service
        self.ef = ef_service

    def _get_patient_or_raise(self, patient_id: Optional[UUID]):
        """Validate patient existence if patient_id is provided."""
        if patient_id is None:
            return None
        patient = self.patient_service.get(patient_id, self.clinician_id)
        if not patient:
            raise ValueError("Patient not found or unauthorized")
        return patient

    # ------------------------------
    # Individual Assessments
    # ------------------------------

    def run_ascvd(self, patient_id: Optional[UUID], input_data: ASCVDRiskInput) -> dict:
        self._get_patient_or_raise(patient_id)
        return run_assessment_pipeline(
            input_schema=input_data,
            db=self.db,
            clinician_id=self.clinician_id,
            model_function=self.ascvd.run_ascvd_prediction,
            assessment_type=AssessmentType.CARDIOLOGY_ASCVD,
            model_name="cardiology_ascvd",
        ).model_dump()

    def run_cha2ds2vasc(self, patient_id: Optional[UUID], input_data: CHA2DS2VAScInput) -> dict:
        self._get_patient_or_raise(patient_id)
        return run_assessment_pipeline(
            input_schema=input_data,
            db=self.db,
            clinician_id=self.clinician_id,
            model_function=self.cha2ds2vasc.run_cha2ds2vasc_prediction,
            assessment_type=AssessmentType.CARDIOLOGY_CHA2DS2VASC,
            model_name="cardiology_cha2ds2vasc",
        ).model_dump()

    def run_bp(self, patient_id: Optional[UUID], input_data: BPCategoryInput) -> dict:
        self._get_patient_or_raise(patient_id)
        return run_assessment_pipeline(
            input_schema=input_data,
            db=self.db,
            clinician_id=self.clinician_id,
            model_function=self.bp.run_bp_category_prediction,
            assessment_type=AssessmentType.CARDIOLOGY_BP,
            model_name="cardiology_bp",
        ).model_dump()

    def run_ecg(self, patient_id: Optional[UUID], input_data: ECGInterpretationInput) -> dict:
        self._get_patient_or_raise(patient_id)
        return run_assessment_pipeline(
            input_schema=input_data,
            db=self.db,
            clinician_id=self.clinician_id,
            model_function=self.ecg.run_ecg_interpretation,
            assessment_type=AssessmentType.CARDIOLOGY_ECG,
            model_name="cardiology_ecg",
        ).model_dump()
    
    def run_ef(self, patient_id: Optional[UUID], input_data: EFInput) -> dict:
        self._get_patient_or_raise(patient_id)
        return run_assessment_pipeline(
            input_schema=input_data,
            db=self.db,
            clinician_id=self.clinician_id,
            model_function=self.ef.run_ef_prediction,
            assessment_type=AssessmentType.CARDIOLOGY_EJECTION_FRACTION,
            model_name="cardiology_ef",
        ).model_dump()

    # ------------------------------
    # Combined Assessment
    # ------------------------------

    def run_full_assessment(
        self,
        patient_id: Optional[UUID],
        ascvd_input: ASCVDRiskInput,
        cha2ds2vasc_input: CHA2DS2VAScInput,
        bp_input: BPCategoryInput,
        ecg_input: ECGInterpretationInput,
        ef_input: EFInput,
    ) -> dict:
        """Run all cardiology assessments together for a patient (patient_id optional)."""
        self._get_patient_or_raise(patient_id)

        return {
            "patient_id": patient_id,
            "ascvd": self.run_ascvd(patient_id, ascvd_input),
            "cha2ds2vasc": self.run_cha2ds2vasc(patient_id, cha2ds2vasc_input),
            "bp_category": self.run_bp(patient_id, bp_input),
            "ecg_result": self.run_ecg(patient_id, ecg_input),
            "ef_result": self.run_ef(patient_id, ef_input),
        }
