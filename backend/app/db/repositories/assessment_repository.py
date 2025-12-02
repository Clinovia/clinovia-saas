from typing import Optional
from sqlalchemy.orm import Session

from app.db.models.assessments import Assessment, AssessmentType
from app.db.repositories.base_repository import BaseRepository


class AssessmentRepository(BaseRepository[Assessment]):
    def __init__(self, db: Session):
        super().__init__(Assessment, db)

    def create(
        self,
        *,
        assessment_type: AssessmentType,  # ✅ renamed from `type`
        patient_id: Optional[int],
        clinician_id: int,
        input_data: dict,
        result: dict,
        algorithm_version: str,
    ) -> Assessment:
        """
        Create a new assessment record.

        Args:
            assessment_type: The type of assessment (e.g., ALZHEIMER_RISK)
            patient_id: ID of the patient (can be None for anonymous assessments)
            clinician_id: ID of the clinician who performed the assessment
            input_data: Raw input data used for the assessment
            result: Computed result/output of the assessment
            algorithm_version: Version of the algorithm/model used

        Returns:
            The persisted Assessment instance
        """
        assessment = Assessment(
            type=assessment_type.value,  # ✅ this is the field in the DB model
            patient_id=patient_id,
            clinician_id=clinician_id,
            input_data=input_data,
            result=result,
            algorithm_version=algorithm_version,
        )

        self.db.add(assessment)
        self.db.commit()
        self.db.refresh(assessment)
        return assessment

    def count_all(self) -> int:
        """Return total number of assessments."""
        return self.db.query(self.model).count()

    def count_by_type(self, assessment_type: str) -> int:
        """Return total number of assessments of a given type."""
        return (
            self.db.query(self.model)
            .filter(self.model.type == assessment_type)
            .count()
        )

    def list_by_patient(self, patient_id: int, skip: int = 0, limit: int = 100):
        """Return assessments for a specific patient."""
        return (
            self.db.query(self.model)
            .filter(self.model.patient_id == patient_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, assessment_id: int) -> Optional[Assessment]:
        """Return a single assessment by ID."""
        return (
            self.db.query(self.model)
            .filter(self.model.id == assessment_id)
            .first()
        )
