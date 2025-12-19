from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

# ----------------------------
# Type alias for Patient ID
# ----------------------------
PatientID = UUID

# ----------------------------
# Shared patient fields
# ----------------------------
class PatientBase(BaseModel):
    first_name: str = Field(..., min_length=1, example="John")
    last_name: str = Field(..., min_length=1, example="Doe")
    date_of_birth: date = Field(..., description="Patient's date of birth")
    gender: str = Field(..., example="male")
    email: Optional[EmailStr] = Field(None, example="john.doe@example.com")
    phone: Optional[str] = Field(None, example="+1234567890")

# ----------------------------
# Schema for creating a patient
# ----------------------------
class PatientCreate(PatientBase):
    """
    Schema for creating a new patient.
    clinician_id is inferred from the authenticated user.
    """
    pass

# ----------------------------
# Schema for updating a patient
# ----------------------------
class PatientUpdate(BaseModel):
    """All fields optional for PATCH updates"""
    first_name: Optional[str] = Field(None, min_length=1)
    last_name: Optional[str] = Field(None, min_length=1)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

# ----------------------------
# Schema for reading a patient (response)
# ----------------------------
class PatientResponse(PatientBase):
    id: PatientID
    clinician_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2

# ----------------------------
# Minimal assessment info for history
# ----------------------------
class AssessmentSummary(BaseModel):
    """Lightweight assessment data for patient history"""
    id: UUID
    type: str  # AssessmentType enum value
    result: dict
    algorithm_version: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ----------------------------
# Schema with assessment history
# ----------------------------
class PatientWithAssessments(PatientResponse):
    assessments: List[AssessmentSummary] = []

    class Config:
        from_attributes = True

# ----------------------------
# List of patients response
# ----------------------------
class PatientList(BaseModel):
    patients: List[PatientResponse]
    total: int

    class Config:
        from_attributes = True

# Resolve forward references
PatientWithAssessments.model_rebuild()
