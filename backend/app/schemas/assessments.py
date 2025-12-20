from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.db.models.assessments import AssessmentType


# =========================
# Shared base (DB-backed)
# =========================
class AssessmentBase(BaseModel):
    specialty: str
    assessment_type: AssessmentType
    patient_id: Optional[UUID] = None
    clinician_id: UUID
    input_data: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    algorithm_version: Optional[str] = None
    status: Optional[str] = "draft"
    notes: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "use_enum_values": True,
    }


# =========================
# Create schema (input)
# =========================
class AssessmentCreate(AssessmentBase):
    pass


# =========================
# Response schema (output)
# =========================
class AssessmentResponse(AssessmentBase):
    id: UUID
    created_at: datetime


# =========================
# List wrapper
# =========================
class AssessmentList(BaseModel):
    assessments: List[AssessmentResponse]
    total: int
