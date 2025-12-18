from typing import Optional
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
        assessment_type: AssessmentType,
        patient_id: Optional[UUID],
        clinician_id: UUID,
        input_data: dict,
        result: Optional[dict] = None,
        algorithm_version: Optional[str] = None,
        status: str = "draft",
        notes: Optional[str] = None,
    ) -> Assessment:
        """
        Create a new assessment record.

        Args:
            assessment_type: The type of assessment (AssessmentType enum)
            patient_id: ID of the patient (optional)
            clinician_id: Supabase user ID / clinician performing the assessment
            input_data: Raw input data used for the assessment
            result: Computed result/output of the assessment
            algorithm_version: Version of the algorithm/model used
            status: Assessment status (default "draft")
            notes: Optional notes

        Returns:
            The persisted Assessment instance
        """
        assessment = Assessment(
            assessment_type=assessment_type,
            patient_id=patient_id,
            clinician_id=clinician_id,
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

    def count_all(self) -> int:
        return self.db.query(self.model).count()

    def count_by_type(self, assessment_type: AssessmentType) -> int:
        return (
            self.db.query(self.model)
            .filter(self.model.assessment_type == assessment_type)
            .count()
        )

    def list_by_patient(
        self, patient_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Assessment]:
        return (
            self.db.query(self.model)
            .filter(self.model.patient_id == patient_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, assessment_id: UUID) -> Optional[Assessment]:
        return (
            self.db.query(self.model)
            .filter(self.model.id == assessment_id)
            .first()
        )
