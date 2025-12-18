from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from app.db.models.assessments import AssessmentType


class AssessmentBase(BaseModel):
    specialty: str
    assessment_type: AssessmentType
    patient_id: Optional[UUID] = None        # Nullable because assessment may not have a patient
    clinician_id: UUID                        # Required
    input_data: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    algorithm_version: Optional[str] = None
    status: Optional[str] = "draft"
    notes: Optional[str] = None

    class Config:
        orm_mode = True
        use_enum_values = True


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentResponse(AssessmentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class AssessmentList(BaseModel):
    assessments: List[AssessmentResponse]
    total: int
