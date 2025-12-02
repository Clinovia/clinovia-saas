# backend/app/services/assessments/cardiology_service.py

from app.services.patients.patient_service import PatientService
from app.schemas.cardiology import (
    ASCVDRiskInput,
    CHA2DS2VAScInput,
    BPCategoryInput,
    ECGInterpretationInput,
)
from app.services.cardiology import (
    ascvd_service,
    bp_service,
    cha2ds2vasc_service,
    ecg_service,
)


class CardiologyAssessmentService:
    """Orchestrates all cardiology assessment workflows."""

    def __init__(self, patient_service: PatientService):
        self.patient_service = patient_service
        self.ascvd = ascvd_service
        self.cha2ds2vasc = cha2ds2vasc_service
        self.bp = bp_service
        self.ecg = ecg_service

    def _get_patient_or_raise(self, patient_id: int):
        """Utility to validate patient existence."""
        patient = self.patient_service.get(patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient

    # ------------------------------
    # Individual Assessments
    # ------------------------------

    def run_ascvd(
        self,
        patient_id: int,
        input_data: ASCVDRiskInput
    ) -> dict:
        """Run ASCVD risk calculation for a patient."""
        self._get_patient_or_raise(patient_id)
        risk = self.ascvd.run_ascvd_prediction(input_data)
        return {
            "patient_id": patient_id,
            "ascvd_risk": risk,
        }

    def run_cha2ds2vasc(
        self,
        patient_id: int,
        input_data: CHA2DS2VAScInput
    ) -> dict:
        """Run CHA₂DS₂-VASc stroke risk calculation for a patient."""
        self._get_patient_or_raise(patient_id)
        score = self.cha2ds2vasc.run_cha2ds2vasc_prediction(input_data)
        return {
            "patient_id": patient_id,
            "cha2ds2vasc_score": score,
        }

    def run_bp(
        self,
        patient_id: int,
        input_data: BPCategoryInput
    ) -> dict:
        """Run blood pressure category classification for a patient."""
        self._get_patient_or_raise(patient_id)
        category = self.bp.run_bp_category_prediction(input_data)
        return {
            "patient_id": patient_id,
            "bp_category": category,
        }

    def run_ecg(
        self,
        patient_id: int,
        input_data: ECGInterpretationInput
    ) -> dict:
        """Run ECG interpretation for a patient."""
        self._get_patient_or_raise(patient_id)
        result = self.ecg.run_ecg_interpretation(input_data)
        return {
            "patient_id": patient_id,
            "ecg_result": result,
        }

    # ------------------------------
    # Combined Assessment
    # ------------------------------

    def run_full_assessment(
        self,
        patient_id: int,
        ascvd_input: ASCVDRiskInput,
        cha2ds2vasc_input: CHA2DS2VAScInput,
        bp_input: BPCategoryInput,
        ecg_input: ECGInterpretationInput,
    ) -> dict:
        """Run all cardiology assessments together for a patient."""
        self._get_patient_or_raise(patient_id)

        return {
            "patient_id": patient_id,
            **self.run_ascvd(patient_id, ascvd_input),
            **self.run_cha2ds2vasc(patient_id, cha2ds2vasc_input),
            **self.run_bp(patient_id, bp_input),
            **self.run_ecg(patient_id, ecg_input),
        }
