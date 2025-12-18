from datetime import datetime, date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModel

if TYPE_CHECKING:
    from app.db.models.assessments import Assessment
    from app.db.models.users import User


class Patient(BaseModel):
    """
    Patient identity record.
    Demographics may be incomplete.
    """

    __tablename__ = "patients"

    # ---- Primary key ----
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ---- Ownership ----
    clinician_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # ---- Demographics (all optional) ----
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # ---- Timestamps ----
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # ---- Relationships ----
    clinician: Mapped["User"] = relationship(
        "User",
        back_populates="patients",
    )

    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        back_populates="patient",
        order_by="Assessment.created_at.desc()",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return (
            f"<Patient id={self.id} "
            f"clinician_id={self.clinician_id}>"
        )
