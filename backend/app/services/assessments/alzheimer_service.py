from typing import Optional
from uuid import UUID
from app.services.patients.patient_service import PatientService
from app.services.alzheimer.diagnosis_screening_service import predict_diag_screen
from app.services.alzheimer.diagnosis_basic_service import predict_diag_basic
from app.services.alzheimer.diagnosis_extended_service import predict_diag_extended
from app.services.alzheimer.prognosis_2yr_basic_service import predict_prog_2yr_basic
from app.services.alzheimer.prognosis_2yr_extended_service import predict_prog_2yr_extended
from app.services.alzheimer.risk_screener_service import assess_alzheimer_risk
from app.services.assessment_pipeline import run_assessment_pipeline
from app.db.models.assessments import AssessmentType


class AlzheimerAssessmentService:
    """Orchestrates Alzheimer's assessment workflows."""

    def __init__(self, patient_service: PatientService, clinician_id: UUID, db_session):
        self.patient_service = patient_service
        self.clinician_id = clinician_id
        self.db = db_session

    def _get_patient_or_raise(self, patient_id: Optional[UUID]):
        """Validate patient existence if patient_id is provided."""
        if patient_id is None:
            return None
        patient = self.patient_service.get(patient_id, self.clinician_id)
        if not patient:
            raise ValueError("Patient not found or unauthorized")
        return patient

    # -----------------------------
    # Diagnosis workflows
    # -----------------------------
    def run_diagnosis_screening(self, patient_id: Optional[UUID], diagnosis_input):
        self._get_patient_or_raise(patient_id)
        return run_assessment_pipeline(
            input_schema=diagnosis_input,
            db=self.db,
            clinician_id=self.clinician_id,
            model_function=predict_diag_screen,
            assessment_type=AssessmentType.ALZHEIMER_DIAGNOSIS_SCREENING,
            model_name="diagnosis_screening",
            model_version="1.0.0",
            use_cache=True,
        )

    def run_diagnosis_basic(self, patient_id: Optional[UUID], diagnosis_input):
        self._get_patient_or_raise(patient_id)
        return run_assessment_pipeline(
            input_schema=diagnosis_input,
            db=self.db,
            clinician_id=self.clinician_id,
            model_function=predict_diag_basic,
            assessment_type=AssessmentType.ALZHEIMER_DIAGNOSIS_BASIC,
            model_name="diagnosis_basic",
            model_version="1.0.0",
            use_cache=True,
        )

    def run_diagnosis_extended(self, patient_id: Optional[UUID], diagnosis_input):
        self._get_patient_or_raise(patient_id)
        return run_assessment_pipeline(
            input_schema=diagnosis_input,
            db=self.db,
            clinician_id=self.clinician_id,
            model_function=predict_diag_extended,
            assessment_type=AssessmentType.ALZHEIMER_DIAGNOSIS_EXTENDED,
            model_name="diagnosis_extended",
            model_version="1.0.0",
            use_cache=True,
        )

    # -----------------------------
    # Prognosis workflows
    # -----------------------------
    def run_prognosis_2yr_basic(self, patient_id: Optional[UUID], prognosis_input):
        self._get_patient_or_raise(patient_id)
        return run_assessment_pipeline(
            input_schema=prognosis_input,
            db=self.db,
            clinician_id=self.clinician_id,
            model_function=predict_prog_2yr_basic,
            assessment_type=AssessmentType.ALZHEIMER_PROGNOSIS_2YR_BASIC,
            model_name="prognosis_2yr_basic",
            model_version="1.0.0",
            use_cache=True,
        )

    def run_prognosis_2yr_extended(self, patient_id: Optional[UUID], prognosis_input):
        self._get_patient_or_raise(patient_id)
        return run_assessment_pipeline(
            input_schema=prognosis_input,
            db=self.db,
            clinician_id=self.clinician_id,
            model_function=predict_prog_2yr_extended,
            assessment_type=AssessmentType.ALZHEIMER_PROGNOSIS_2YR_EXTENDED,
            model_name="prognosis_2yr_extended",
            model_version="1.0.0",
            use_cache=True,
        )

    # -----------------------------
    # Risk assessment
    # -----------------------------
    def run_risk_screener(self, patient_id: Optional[UUID], risk_input):
        self._get_patient_or_raise(patient_id)
        return run_assessment_pipeline(
            input_schema=risk_input,
            db=self.db,
            clinician_id=self.clinician_id,
            model_function=assess_alzheimer_risk,
            assessment_type=AssessmentType.ALZHEIMER_RISK,
            model_name="risk_screener",
            model_version="1.0.0",
            use_cache=True,
        )
