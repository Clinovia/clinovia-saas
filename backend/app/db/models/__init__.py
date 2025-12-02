# backend/app/db/models/__init__.py

# Import all models so they are registered with Base.metadata
from .users import User
from .patients import Patient
from .assessments import Assessment

__all__ = ["User", "Patient", "Assessment"]
