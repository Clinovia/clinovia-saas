from typing import Optional, List, Tuple, Union
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.db.models.patients import Patient
from app.db.repositories.patient_repository import PatientRepository
from app.schemas.patients import PatientCreate, PatientUpdate
from datetime import date


class PatientService:
    """Service layer for patient CRUD operations with clinician authorization."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = PatientRepository(db)

    # ========================================
    # READ Operations
    # ========================================

    def get(self, patient_id: Optional[UUID], clinician_id: UUID) -> Optional[Patient]:
        """
        Fetch a patient by ID if it belongs to the requesting clinician.
        Returns None if not found or unauthorized.
        """
        if not patient_id:
            return None

        patient = self.repo.get(patient_id)
        if patient and patient.clinician_id != clinician_id:
            return None

        return patient

    def get_with_assessments(
        self, patient_id: Optional[UUID], clinician_id: UUID
    ) -> Optional[Patient]:
        """
        Fetch a patient with all their assessments eagerly loaded.
        Returns None if not found or unauthorized.
        """
        if not patient_id:
            return None

        return (
            self.db.query(Patient)
            .options(joinedload(Patient.assessments))
            .filter(
                Patient.id == patient_id,
                Patient.clinician_id == clinician_id
            )
            .first()
        )

    def list_by_clinician(
        self,
        clinician_id: UUID,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> Tuple[List[Patient], int]:
        """
        Get all patients for a clinician, optionally filtered by search term.
        Returns a tuple of (patients list, total count).
        """
        query = self.db.query(Patient).filter(Patient.clinician_id == clinician_id)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Patient.first_name.ilike(search_term)) |
                (Patient.last_name.ilike(search_term))
            )

        total = query.count()
        patients = query.order_by(Patient.created_at.desc()).offset(skip).limit(limit).all()
        return patients, total

    # ========================================
    # CREATE Operations
    # ========================================

    def create(self, patient_data: PatientCreate, clinician_id: UUID) -> Patient:
        """
        Create a new patient record for the specified clinician.
        """
        patient_dict = patient_data.model_dump()
        patient_dict['clinician_id'] = clinician_id

        # Create a temporary object to pass to repository
        from types import SimpleNamespace
        obj_with_dict = SimpleNamespace(**patient_dict)
        obj_with_dict.dict = lambda: patient_dict

        return self.repo.create(obj_with_dict)

    # ========================================
    # UPDATE Operations
    # ========================================

    def update(
        self,
        patient_id: UUID,
        updates: PatientUpdate,
        clinician_id: UUID
    ) -> Optional[Patient]:
        """
        Update patient details if the clinician is authorized.
        """
        patient = self.get(patient_id, clinician_id)
        if not patient:
            return None

        update_dict = updates.model_dump(exclude_unset=True)
        if not update_dict:
            return patient

        return self.repo.update(patient, update_dict)

    # ========================================
    # DELETE Operations
    # ========================================

    def delete(self, patient_id: UUID, clinician_id: UUID) -> bool:
        """
        Delete a patient if the clinician is authorized.
        """
        patient = self.get(patient_id, clinician_id)
        if not patient:
            return False

        self.repo.delete(patient)
        return True

    # ========================================
    # HELPER Methods
    # ========================================

    @staticmethod
    def calculate_age(date_of_birth: date) -> int:
        """
        Calculate current age from date of birth.
        """
        today = date.today()
        age = today.year - date_of_birth.year
        if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
            age -= 1
        return age

    def get_patient_age(self, patient_id: UUID, clinician_id: UUID) -> Optional[int]:
        """
        Get a patient's current age, or None if not found or date_of_birth missing.
        """
        patient = self.get(patient_id, clinician_id)
        if not patient or not patient.date_of_birth:
            return None
        return self.calculate_age(patient.date_of_birth)
