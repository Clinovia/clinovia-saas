from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.db.base import BaseModel
import enum, uuid
from datetime import datetime


class AssessmentType(str, enum.Enum):
    """
    Assessment types.

    Python enum names are namespaced by specialty for clarity.
    Stored DB values are normalized and DO NOT include specialty.
    """

    # --------------------
    # Alzheimer
    # --------------------
    ALZHEIMER_DIAGNOSIS_SCREENING = "diagnosis_screening"
    ALZHEIMER_DIAGNOSIS_BASIC = "diagnosis_basic"
    ALZHEIMER_DIAGNOSIS_EXTENDED = "diagnosis_extended"
    ALZHEIMER_PROGNOSIS_2YR_BASIC = "prognosis_2yr_basic"
    ALZHEIMER_PROGNOSIS_2YR_EXTENDED = "prognosis_2yr_extended"
    ALZHEIMER_RISK_SCREENER = "risk_screener"

    # --------------------
    # Cardiology
    # --------------------
    CARDIOLOGY_ASCVD = "ascvd"
    CARDIOLOGY_BP = "bp_categories"
    CARDIOLOGY_CHA2DS2VASC = "cha2ds2vasc"
    CARDIOLOGY_ECG = "ecg"
    CARDIOLOGY_EJECTION_FRACTION = "ejection_fraction"


class Assessment(BaseModel):
    __tablename__ = "assessments"

    # --------------------
    # Core Fields
    # --------------------
    specialty = Column(
        String,
        nullable=False,
        index=True,
        doc="Clinical specialty (e.g. alzheimer, cardiology)"
    )

    assessment_type = Column(
        Enum(AssessmentType),
        nullable=False,
        index=True,
        doc="Normalized assessment type (no specialty prefix)"
    )

    assessment_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # --------------------
    # Foreign Keys
    # --------------------
    patient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("patients.id", ondelete="SET NULL"),
        nullable=True
    )

    clinician_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    # --------------------
    # Data Payload
    # --------------------
    input_data = Column(JSONB, nullable=False)
    result = Column(JSONB)

    algorithm_version = Column(String(50))
    status = Column(String, default="draft")
    notes = Column(String)

    # --------------------
    # Relationships
    # --------------------
    patient = relationship("Patient", back_populates="assessments")
    clinician = relationship("User", back_populates="assessments")
