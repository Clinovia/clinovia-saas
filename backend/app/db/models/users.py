from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModel

if TYPE_CHECKING:
    from app.db.models.patients import Patient
    from app.db.models.assessments import Assessment


class User(BaseModel):
    """
    Application-level user (clinician / admin).
    Auth is handled by Supabase auth.users.
    """

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

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

    patients: Mapped[List["Patient"]] = relationship(
        "Patient",
        back_populates="created_by",
        passive_deletes=True,
    )

    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        back_populates="clinician",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
