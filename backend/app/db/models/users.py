from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import DateTime, String, func
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

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    patients: Mapped[List["Patient"]] = relationship(
        "Patient",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    assessments: Mapped[List["Assessment"]] = relationship(
        "Assessment",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    alzheimer_assessments: Mapped[List["AlzheimerAssessment"]] = relationship(
        "AlzheimerAssessment",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    cardiology_assessments: Mapped[List["CardiologyAssessment"]] = relationship(
        "CardiologyAssessment",
        back_populates="user",
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
        return f"<User(id={self.id}, email={self.email})>"
