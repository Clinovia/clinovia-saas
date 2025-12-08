from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import BaseModel

class CardiologyAssessment(BaseModel):
    __tablename__ = "cardiology_assessments"

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    ascvd_score = Column(Float, nullable=True)
    bp_category = Column(String, nullable=True)
    cha2ds2vasc_score = Column(Float, nullable=True)
    ecg_interpretation = Column(String, nullable=True)
    ejection_fraction = Column(Float, nullable=True)

    # Relationship back to patient
    patient = relationship("Patient", back_populates="cardiology_assessments")
