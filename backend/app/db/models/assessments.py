# backend/app/db/models/assessments.py
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Enum, cast
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import enum

class AssessmentType(str, enum.Enum):
    ALZHEIMER_DIAGNOSIS_SCREENING = "alzheimer_diagnosis_screening"
    ALZHEIMER_DIAGNOSIS_BASIC = "alzheimer_diagnosis_basic"
    ALZHEIMER_DIAGNOSIS_EXTENDED = "alzheimer_diagnosis_extended"
    ALZHEIMER_PROGNOSIS_2YR_BASIC = "alzheimer_prognosis_2yr_basic"
    ALZHEIMER_PROGNOSIS_2YR_EXTENDED = "alzheimer_prognosis_2yr_extended"
    ALZHEIMER_RISK = "alzheimer_risk_screener"
    CARDIOLOGY_ASCVD = "cardiology_ascvd"
    CARDIOLOGY_BP = "cardiology_bp_categories"
    CARDIOLOGY_CHA2DS2VASC = "cardiology_cha2ds2vasc"
    CARDIOLOGY_ECG = "cardiology_ecg"
    CARDIOLOGY_EJECTION_FRACTION = "cardiology_ejection_fraction"

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(AssessmentType), nullable=False, index=True)
    patient_id = Column(String, nullable=True)  # Can be "N/A", "123", or None
    clinician_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    input_data = Column(JSON, nullable=False)
    result = Column(JSON, nullable=False)
    algorithm_version = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    patient = relationship(
        "Patient",
        primaryjoin="cast(remote(Patient.id), String) == foreign(Assessment.patient_id)",
        back_populates="assessments",
        viewonly=True,
    )
    clinician = relationship("User", back_populates="assessments")

    def __repr__(self):
        return f"<Assessment(id={self.id}, type={self.type}, patient_id={self.patient_id}, clinician_id={self.clinician_id})>"