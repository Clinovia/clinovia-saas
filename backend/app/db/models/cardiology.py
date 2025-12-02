from sqlalchemy import String, Column, Float, ForeignKey, Integer

from .patients import Base


class CardiologyAssessment(Base):
    __tablename__ = "cardiology_assessments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    ascvd_score = Column(Float)
    bp_category = Column(String)
    cha2ds2vasc_score = Column(Float)
    ecg_interpretation = Column(String)
    ejection_fraction = Column(Float)
