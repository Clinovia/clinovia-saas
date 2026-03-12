from pydantic import BaseModel
from datetime import date


class AlzheimerReport(BaseModel):
    patient_id: str
    test_date: date
    risk_score: float
    diagnosis: str


class AlzheimerReportResponse(BaseModel):
    reports: list[AlzheimerReport]
