from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import BaseModel

if TYPE_CHECKING:
    from app.db.models.patients import Patient
    from app.db.models.assessments import Assessment
    from app.db.models.alzheimer import AlzheimerAssessment
    from app.db.models.cardiology import CardiologyAssessment
    from app.db.models.api_keys import APIKey
    from app.db.models.billing import Subscription, Payment


class User(BaseModel):
    __tablename__ = "users"

    # Basic info
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Account status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Company / role info
    company: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    team_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    enterprise_interest: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Trial / subscription info
    trial_start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), default=func.now())
    trial_end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subscription_status: Mapped[str] = mapped_column(String, default="trial", nullable=False)

    # Relationships
    patients: Mapped[List["Patient"]] = relationship(
        "Patient",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        back_populates="clinician",
        cascade="all, delete-orphan"
    )
    alzheimer_assessments: Mapped[List["AlzheimerAssessment"]] = relationship(
        "AlzheimerAssessment",
        back_populates="clinician",
        cascade="all, delete-orphan"
    )
    cardiology_assessments: Mapped[List["CardiologyAssessment"]] = relationship(
        "CardiologyAssessment",
        back_populates="clinician",
        cascade="all, delete-orphan"
    )
    api_keys: Mapped[List["APIKey"]] = relationship(
        "APIKey",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    subscriptions: Mapped[List["Subscription"]] = relationship(
        "Subscription",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    payments: Mapped[List["Payment"]] = relationship(
        "Payment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.full_name})>"
