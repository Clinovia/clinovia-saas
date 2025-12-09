from datetime import datetime, date
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, cast
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import BaseModel

if TYPE_CHECKING:
    from app.db.models.assessments import Assessment
    from app.db.models.alzheimer import AlzheimerAssessment
    from app.db.models.cardiology import CardiologyAssessment
    from app.db.models.users import User


class Patient(BaseModel):
    __tablename__ = "patients"

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="patients")

    # Assessments
    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        primaryjoin="cast(Patient.id, String) == foreign(Assessment.patient_id)",
        back_populates="patient",
        viewonly=True,
        order_by="Assessment.created_at.desc()"
    )

    alzheimer_assessments: Mapped[List["AlzheimerAssessment"]] = relationship(
        "AlzheimerAssessment",
        back_populates="patient",
        order_by="AlzheimerAssessment.id.desc()"
    )

    cardiology_assessments: Mapped[List["CardiologyAssessment"]] = relationship(
        "CardiologyAssessment",
        back_populates="patient"
    )

    def __repr__(self) -> str:
        return f"<Patient(id={self.id}, name={self.first_name} {self.last_name}, user_id={self.user_id})>"
