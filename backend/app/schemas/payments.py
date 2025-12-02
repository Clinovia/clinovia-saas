from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PaymentCreate(BaseModel):
    amount: float

class PaymentResponse(BaseModel):
    id: int
    amount: float
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
