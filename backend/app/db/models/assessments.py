from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.db.base import BaseModel
import enum, uuid
from datetime import datetime

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

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Core fields
    specialty = Column(String, nullable=False)
    assessment_type = Column(Enum(AssessmentType), nullable=False, index=True)
    assessment_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Foreign Keys
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="SET NULL"), nullable=True)
    clinician_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)

    # Data
    input_data = Column(JSONB, nullable=False)
    result = Column(JSONB)
    algorithm_version = Column(String(50))
    status = Column(String, default="draft")
    notes = Column(String)

    # Relationships
    patient = relationship("Patient", back_populates="assessments")
    clinician = relationship("User", back_populates="assessments")
