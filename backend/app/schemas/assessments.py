from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, List, Optional
from app.db.models.assessments import AssessmentType

class AssessmentBase(BaseModel):
    specialty: str
    assessment_type: AssessmentType
    patient_id: int
    clinician_id: Optional[int] = None
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
    id: int
    created_at: datetime
    updated_at: datetime

class AssessmentList(BaseModel):
    assessments: List[AssessmentResponse]
    total: int
