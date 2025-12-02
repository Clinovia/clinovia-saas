from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.db.models.assessments import AssessmentType


class AssessmentBase(BaseModel):
    type: AssessmentType
    patient_id: int  # Matches the database model
    clinician_id: Optional[int] = None  # Matches the database model
    input_data: Dict[str, Any]
    result: Dict[str, Any]
    algorithm_version: Optional[str] = None

    class Config:
        # Allows Pydantic to read SQLAlchemy model attributes
        orm_mode = True
        use_enum_values = True  # stores enums as their values (string/int) in JSON


class AssessmentCreate(AssessmentBase):
    """For creating a new assessment; DB will assign ID and timestamps."""
    pass


class AssessmentResponse(AssessmentBase):
    id: int
    created_at: datetime
    updated_at: datetime


class AssessmentList(BaseModel):
    assessments: List[AssessmentResponse]
    total: int