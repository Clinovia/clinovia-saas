from app.services.patients.patient_service import PatientService
from app.services.alzheimer.diagnosis_screening_service import predict_diag_screen
from app.services.alzheimer.diagnosis_basic_service import predict_diag_basic
from app.services.alzheimer.diagnosis_extended_service import predict_diag_extended
from app.services.alzheimer.prognosis_2yr_basic_service import predict_prog_2yr_basic
from app.services.alzheimer.prognosis_2yr_extended_service import predict_prog_2yr_extended
from app.services.alzheimer.risk_screener_service import assess_alzheimer_risk

from app.schemas.alzheimer.diagnosis_screening import AlzheimerDiagnosisInput
from app.schemas.alzheimer.diagnosis_basic import AlzheimerDiagnosisBasicInput
from app.schemas.alzheimer.diagnosis_extended import AlzheimerDiagnosisExtendedInput
from app.schemas.alzheimer.prognosis_2yr_basic import AlzheimerPrognosis2yrBasicInput
from app.schemas.alzheimer.prognosis_2yr_extended import AlzheimerPrognosis2yrExtendedInput
from app.schemas.alzheimer.risk_screener import AlzheimerRiskScreenerInput

class AlzheimerAssessmentService:
    """Orchestrates Alzheimer's assessment workflows."""

    def __init__(self, patient_service: PatientService):
        self.patient_service = patient_service

    # -----------------------------
    # Diagnosis workflows
    # -----------------------------
    def run_diagnosis_screening(
        self,
        patient_id: int,
        diagnosis_input: AlzheimerDiagnosisInput
    ) -> dict:
        """Run cognitive screening model for a patient."""
        patient = self.patient_service.get_patient(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        diagnosis = predict_diag_screen(diagnosis_input)

        return {
            "patient_id": patient_id,
            "diagnosis": diagnosis,
        }

    def run_diagnosis_basic(
        self,
        patient_id: int,
        diagnosis_input: AlzheimerDiagnosisBasicInput
    ) -> dict:
        """Run basic Alzheimer's diagnosis model."""
        patient = self.patient_service.get_patient(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        diagnosis = predict_diag_basic(diagnosis_input)

        return {
            "patient_id": patient_id,
            "diagnosis": diagnosis,
        }

    def run_diagnosis_extended(
        self,
        patient_id: int,
        diagnosis_input: AlzheimerDiagnosisExtendedInput
    ) -> dict:
        """Run extended Alzheimer's diagnosis model with multimodal features."""
        patient = self.patient_service.get_patient(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        diagnosis = predict_diag_extended(diagnosis_input)

        return {
            "patient_id": patient_id,
            "diagnosis": diagnosis,
        }

    # -----------------------------
    # Prognosis workflows
    # -----------------------------
    def run_prognosis_2yr_basic(
        self,
        patient_id: int,
        prognosis_input: AlzheimerPrognosis2yrBasicInput
    ) -> dict:
        """Predict 2-year progression using basic clinical features."""
        patient = self.patient_service.get_patient(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        prognosis = predict_prog_2yr_basic(prognosis_input)

        return {
            "patient_id": patient_id,
            "prognosis_2yr_basic": prognosis,
        }

    def run_prognosis_2yr_extended(
        self,
        patient_id: int,
        prognosis_input: AlzheimerPrognosis2yrExtendedInput
    ) -> dict:
        """Predict 2-year progression using extended multimodal features."""
        patient = self.patient_service.get_patient(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        prognosis = predict_prog_2yr_extended(prognosis_input)

        return {
            "patient_id": patient_id,
            "prognosis_2yr_extended": prognosis,
        }

    # -----------------------------
    # Risk assessment
    # -----------------------------
    def run_risk_screener(
        self,
        patient_id: int,
        risk_input: AlzheimerRiskScreenerInput
    ) -> dict:
        """Run Alzheimer's risk screener for a patient."""
        patient = self.patient_service.get_patient(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        risk = assess_alzheimer_risk(risk_input)

        return {
            "patient_id": patient_id,
            "risk_score": risk,
        }
