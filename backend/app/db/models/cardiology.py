from typing import TYPE_CHECKING, Dict, Any
from sqlalchemy import String, JSON, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import BaseModel
from app.db.models.assessments import AssessmentType

if TYPE_CHECKING:
    from app.db.models.users import User
    from app.db.models.patients import Patient


class CardiologyAssessment(BaseModel):
    __tablename__ = "cardiology_assessments"

    # --- Assessment type ---
    type: Mapped[AssessmentType] = mapped_column(
        Enum(AssessmentType, name="assessment_type_enum"),
        nullable=False,
        index=True
    )

    # --- Foreign keys ---
    patient_id: Mapped[int | None] = mapped_column(
        ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    clinician_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # --- JSON fields ---
    input_data: Mapped[Dict[str, Any]] = mapped_column(
        JSON, nullable=False, default=dict
    )
    result: Mapped[Dict[str, Any]] = mapped_column(
        JSON, nullable=False, default=dict
    )

    # --- Algorithm version ---
    algorithm_version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    # --- Relationships ---
    patient: Mapped["Patient | None"] = relationship(
        "Patient", back_populates="cardiology_assessments"
    )
    clinician: Mapped["User"] = relationship(
        "User", back_populates="cardiology_assessments"
    )

    def __repr__(self) -> str:
        return f"<CardiologyAssessment(id={self.id}, type={self.type}, patient_id={self.patient_id})>"
