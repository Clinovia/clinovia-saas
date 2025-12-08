from sqlalchemy import Column, Integer, String, JSON, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
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

class Assessment(BaseModel):
    __tablename__ = "assessments"

    type = Column(Enum(AssessmentType), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    clinician_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    input_data = Column(JSON, nullable=False)
    result = Column(JSON, nullable=False)
    algorithm_version = Column(String(50), nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="assessments")
    clinician = relationship("User", back_populates="assessments")
