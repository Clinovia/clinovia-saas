from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.models.patients import Patient


class PatientRepository:
    def __init__(self, db: Session):
        self.db = db
        self.model = Patient

    def create(
        self,
        *,
        clinician_id: UUID,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        date_of_birth: Optional[str] = None,
        gender: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Patient:
        """
        Create a new patient record.
        """
        patient = Patient(
            clinician_id=clinician_id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            email=email,
            phone=phone,
        )
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def get_by_id(self, patient_id: UUID) -> Optional[Patient]:
        return self.db.query(self.model).filter(self.model.id == patient_id).first()

    def list_by_clinician(
        self, clinician_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Patient]:
        return (
            self.db.query(self.model)
            .filter(self.model.clinician_id == clinician_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count_by_clinician(self, clinician_id: UUID) -> int:
        return (
            self.db.query(self.model)
            .filter(self.model.clinician_id == clinician_id)
            .count()
        )
