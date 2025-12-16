from typing import Optional, List
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
    
    def get(self, patient_id: int, user_id: UUID) -> Optional[Patient]:
        """
        Fetch a patient by ID, ensuring it belongs to the requesting clinician.
        
        Args:
            patient_id: The patient's ID
            user_id: The clinician's user ID (for authorization)
        
        Returns:
            Patient if found and authorized, None otherwise
        """
        patient = self.repo.get(patient_id)
        
        # ✅ Authorization check
        if patient and patient.user_id != user_id:
            return None  # Clinician doesn't own this patient
        
        return patient
    
    def get_with_assessments(self, patient_id: int, user_id: UUID) -> Optional[Patient]:
        """
        Fetch a patient with their full assessment history.
        
        Args:
            patient_id: The patient's ID
            user_id: The clinician's user ID (for authorization)
        
        Returns:
            Patient with assessments eagerly loaded
        """
        patient = self.db.query(Patient).options(
            joinedload(Patient.assessments)
        ).filter(
            Patient.id == patient_id,
            Patient.user_id == user_id  # ✅ Authorization at query level
        ).first()
        
        return patient
    
    def list_by_clinician(
        self, 
        user_id: UUID, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None
    ) -> tuple[List[Patient], int]:
        """
        Get all patients for a specific clinician with optional search.
        
        Args:
            user_id: The clinician's user ID
            skip: Number of records to skip (pagination)
            limit: Maximum number of records to return
            search: Optional search term for name filtering
        
        Returns:
            Tuple of (patients list, total count)
        """
        query = self.db.query(Patient).filter(Patient.user_id == user_id)
        
        # ✅ Optional search filter
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
    
    def create(self, patient_data: PatientCreate, user_id: UUID) -> Patient:
        # Create a new Pydantic model with user_id added
        patient_dict = patient_data.model_dump()
        patient_dict['user_id'] = user_id
        
        # Don't create ORM object - let repository do it
        # Create a temporary dict-like object
        from types import SimpleNamespace
        obj_with_dict = SimpleNamespace(**patient_dict)
        obj_with_dict.dict = lambda: patient_dict
        
        return self.repo.create(obj_with_dict)
    
    # ========================================
    # UPDATE Operations
    # ========================================
    
    def update(
        self, 
        patient_id: int, 
        updates: PatientUpdate, 
        user_id: UUID
    ) -> Optional[Patient]:
        """
        Update patient details, ensuring clinician owns the patient.
        
        Args:
            patient_id: The patient's ID
            updates: Validated update data from schema
            user_id: The clinician's user ID (for authorization)
        
        Returns:
            Updated Patient if successful, None if not found/unauthorized
        """
        patient = self.get(patient_id, user_id)
        
        if not patient:
            return None
        
        # ✅ Only update fields that were provided
        update_dict = updates.model_dump(exclude_unset=True)
        
        if not update_dict:
            return patient  # No changes requested
        
        return self.repo.update(patient, update_dict)
    
    # ========================================
    # DELETE Operations
    # ========================================
    
    def delete(self, patient_id: int, user_id: UUID) -> bool:
        """
        Delete a patient, ensuring clinician owns the patient.
        
        Args:
            patient_id: The patient's ID
            user_id: The clinician's user ID (for authorization)
        
        Returns:
            True if deleted successfully, False if not found/unauthorized
        """
        patient = self.get(patient_id, user_id)
        
        if not patient:
            return False
        
        self.repo.delete(patient)
        return True
    
    # ========================================
    # HELPER Methods
    # ========================================
    
    def calculate_age(self, date_of_birth: date) -> int:
        """Calculate current age from date of birth."""
        today = date.today()
        age = today.year - date_of_birth.year
        
        # Adjust if birthday hasn't occurred this year
        if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
            age -= 1
        
        return age
    
    def get_patient_age(self, patient_id: int, user_id: UUID) -> Optional[int]:
        """Get a patient's current age."""
        patient = self.get(patient_id, user_id)
        
        if not patient:
            return None
        
        return self.calculate_age(patient.date_of_birth)