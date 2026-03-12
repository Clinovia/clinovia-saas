from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AlzheimerBatchCreateResponse(BaseModel):
    batch_id: str
    status: str


class AlzheimerBatchStatusResponse(BaseModel):
    batch_id: str
    status: str
    submitted_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
