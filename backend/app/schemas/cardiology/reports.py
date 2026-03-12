
    
from pydantic import BaseModel
from datetime import date
from typing import Optional


class CardiologyReport(BaseModel):
    patient_id: str
    test_date: date
    ascvd_risk: Optional[float] = None
    bp_category: Optional[str] = None


class CardiologyReportResponse(BaseModel):
    reports: list[CardiologyReport]

