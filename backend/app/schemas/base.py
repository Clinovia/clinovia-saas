from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class BaseSchema(BaseModel):
    model_config = {
        "protected_namespaces": (),
        "from_attributes": True  # Allows reading from SQLAlchemy objects
    }

class AssessmentInputSchema(BaseSchema):
    """Base schema for assessment inputs."""
    patient_id: Optional[int] = None

class AssessmentOutputSchema(BaseSchema):
    """Base schema for assessment outputs."""
    prediction_id: str
    model_name: str
    status: str
    result: Dict[str, Any]
    created_at: Optional[datetime] = None
