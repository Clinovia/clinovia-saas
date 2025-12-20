# backend/app/db/repositories/assessment_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.models.assessments import Assessment, AssessmentType


class AssessmentRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Assessment

    def create(
        self,
        *,
        specialty: str,
        assessment_type: AssessmentType,
        clinician_id: UUID,
        patient_id: Optional[UUID],
        input_data: dict,
        result: Optional[dict] = None,
        algorithm_version: Optional[str] = None,
        status: str = "draft",
        notes: Optional[str] = None,
    ) -> Assessment:
        """
        Create a new assessment record.

        Design
        -------
        - specialty is stored explicitly (e.g. "alzheimer", "cardiology")
        - assessment_type stores ONLY the normalized enum value
          (e.g. "ascvd", "diagnosis_basic")

        Args:
            specialty: Clinical specialty
            assessment_type: AssessmentType enum
            clinician_id: Clinician (user) ID
            patient_id: Optional patient ID (nullable)
            input_data: Raw input payload
            result: Computed assessment result
            algorithm_version: Algorithm/model version
            status: Assessment status (default: draft)
            notes: Optional clinician notes
        """
        assessment = self.model(
            specialty=specialty,
            assessment_type=assessment_type,
            clinician_id=clinician_id,
            patient_id=patient_id,
            input_data=input_data,
            result=result,
            algorithm_version=algorithm_version,
            status=status,
            notes=notes,
        )

        self.db.add(assessment)
        self.db.commit()
        self.db.refresh(assessment)
        return assessment

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_by_id(self, assessment_id: UUID) -> Optional[Assessment]:
        return (
            self.db.query(self.model)
            .filter(self.model.id == assessment_id)
            .first()
        )

    def list_by_patient(
        self,
        patient_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Assessment]:
        return (
            self.db.query(self.model)
            .filter(self.model.patient_id == patient_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_by_specialty(
        self,
        specialty: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Assessment]:
        return (
            self.db.query(self.model)
            .filter(self.model.specialty == specialty)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_all(self) -> int:
        return self.db.query(self.model).count()

    def count_by_type(self, assessment_type: AssessmentType) -> int:
        return (
            self.db.query(self.model)
            .filter(self.model.assessment_type == assessment_type)
            .count()
        )

    def count_by_specialty(self, specialty: str) -> int:
        return (
            self.db.query(self.model)
            .filter(self.model.specialty == specialty)
            .count()
        )
