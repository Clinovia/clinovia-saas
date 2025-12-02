# backend/app/services/patients/history_service.py

from typing import List
from app.services.patients.patient_service import PatientService
from app.schemas.assessments import AssessmentResponse  # use your existing Pydantic model

class HistoryService:
    """Aggregates patient assessment history."""

    def __init__(self, patient_service: PatientService):
        self.patient_service = patient_service
        self._assessment_history: dict[str, List[AssessmentResponse]] = {}

    def add_assessment(self, patient_id: str, assessment: AssessmentResponse):
        self._assessment_history.setdefault(patient_id, []).append(assessment)

    def get_history(self, patient_id: str) -> List[AssessmentResponse]:
        return self._assessment_history.get(patient_id, [])
