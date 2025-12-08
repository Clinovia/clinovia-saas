# backend/app/db/base.py
"""
SQLAlchemy declarative base and common mixins.

Provides:
- Base class for all SQLAlchemy models
- Common mixins (ID, timestamps, soft delete)
- Utility methods for models
- Automatic table name generation
- Supabase-compatible for PostgreSQL
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import func

# 1️⃣ Declarative Base
Base = declarative_base()


# 2️⃣ Mixins
class IDMixin:
    """Adds an integer primary key 'id' column"""
    id = Column(Integer, primary_key=True, index=True)


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
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
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
        name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        if not name.endswith('s'):
            name += 's'
        return name


# 3️⃣ BaseModel with ID, timestamps, table name, and utility methods
class BaseModel(Base, IDMixin, TimestampMixin, TableNameMixin):
    """
    Base model with:
    - Integer primary key `id`
    - created_at and updated_at timestamps
    - Automatic __tablename__ generation
    - to_dict() utility method
    - __repr__ method
    """
    __abstract__ = True

    def to_dict(self):
        """Convert model to dictionary"""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = ', '.join(
            f"{key}={value!r}"
            for key, value in self.to_dict().items()
            if key != 'hashed_password'
        )
        return f"<{class_name}({attributes})>"


