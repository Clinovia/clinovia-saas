# backend/app/db/base.py
"""
SQLAlchemy declarative base and common mixins.

Provides:
- Base class for all SQLAlchemy models
- Common mixins (timestamps, soft delete)
- Utility methods for models
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import func

# 1️⃣ Define Base here — no imports from models
Base = declarative_base()


# 2️⃣ Mixins
class TimestampMixin:
    """Adds created_at and updated_at timestamps"""
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True
    )


class SoftDeleteMixin:
    """Adds soft delete functionality"""
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)

    def soft_delete(self):
        """Mark record as deleted"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

    def restore(self):
        """Restore soft-deleted record"""
        self.is_deleted = False
        self.deleted_at = None


class TableNameMixin:
    """Automatically generate __tablename__ from class name"""
    @declared_attr
    def __tablename__(cls):
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        if not name.endswith('s'):
            name = name + 's'
        return name


class BaseModel(Base, TimestampMixin):
    """
    Enhanced base model with timestamps, dict conversion, and repr.
    """
    __abstract__ = True

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = ', '.join(
            f"{key}={value!r}"
            for key, value in self.to_dict().items()
            if key != 'hashed_password'
        )
        return f"<{class_name}({attributes})>"


# 3️⃣ Optional: Import models after Base defined
# This ensures relationships work and avoids circular imports
try:
    import app.db.models.users
    import app.db.models.patients
    import app.db.models.assessments
except ImportError:
    # During testing, models may not yet exist — ignore
    pass


__all__ = [
    "Base",
    "BaseModel",
    "TimestampMixin",
    "SoftDeleteMixin",
    "TableNameMixin",
]
