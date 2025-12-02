"""
Patient History Service

Aggregates past assessments across multiple domains for a single patient.
"""

from app.services.patients.patient_service import PatientService


class PatientHistoryService:
    def __init__(self, patient_service: PatientService):
        self.patient_service = patient_service

    def get_history(self, patient_id: str) -> dict:
        patient = self.patient_service.get_patient(patient_id)
        if not patient:
            raise ValueError("Patient not found")

        # Placeholder for historical retrieval logic
        return {
            "alzheimer_assessments": patient.get("alzheimer_history", []),
            "cardiology_assessments": patient.get("cardiology_history", []),
        }
