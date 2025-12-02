# app/db/models/assessments.py
from sqlalchemy import Column, Integer, String, JSON, Enum
from app.db.base import Base
from app.db.models.assessments import AssessmentType

class AlzheimerAssessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(AssessmentType), nullable=False)  # ← column name is "type"
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    clinician_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    input_data = Column(JSON)
    result = Column(JSON)
    algorithm_version = Column(String)