# backend/app/db/models/__init__.py
# Import all models so they are registered with Base.metadata
from .users import User
from .patients import Patient
from .assessments import Assessment
from .alzheimer import AlzheimerAssessment
from .cardiology import CardiologyAssessment
from .api_keys import APIKey
from .billing import Subscription, Payment
from .analytics import ApiUsageLog

__all__ = [
    "User",
    "Patient", 
    "Assessment",
    "AlzheimerAssessment",
    "CardiologyAssessment",
    "APIKey",
    "Subscription",
    "Payment",
    "ApiUsageLog",
]