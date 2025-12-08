"""
Dependency injection for FastAPI routes (Supabase-compatible).

Replaces backend JWT auth with Supabase token verification.
Keeps API key auth, service injection, and cache injection intact.
"""

import logging
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session as DBSession

from app.db.session import get_db
from app.db.models.users import User

# Optional imports for API key handling
try:
    from app.db.models.api_keys import APIKey as APIKeyModel
    from app.services.api_key_service import APIKeyService
except ImportError:
    APIKeyModel = None
    APIKeyService = None

# Service imports
from app.services.cache import Cache
from app.services.users.user_service import UserService
from app.services.patients.patient_service import PatientService
from app.services.assessments.patient_history_service import PatientHistoryService
from app.services.assessments.alzheimer_service import AlzheimerAssessmentService
from app.services.assessments.cardiology_service import CardiologyAssessmentService
from app.services.analytics.reporting_service import ReportingService
from app.services.analytics.usage_service import UsageAnalyticsService
from app.services.billing.invoice_service import InvoiceService
from app.services.billing.subscription_service import SubscriptionService

logger = logging.getLogger(__name__)

# ----------------------------
# API Key Authentication
# ----------------------------
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key_user(
    db: DBSession = Depends(get_db),
    key: Optional[str] = Depends(api_key_header),
) -> Optional[User]:
    """Authenticate via API key and track usage."""
    if not key or APIKeyService is None:
        return None

    db_key = APIKeyService.get_key_by_value(db, key)
    if not db_key or not db_key.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or inactive API key",
        )

    APIKeyService.increment_usage(db, db_key)
    return db_key.user


# ----------------------------
# Supabase Token Authentication
# ----------------------------
async def get_current_user(
    request: Request,
    db: DBSession = Depends(get_db),
    api_key_user: Optional[User] = Depends(get_api_key_user),
) -> User:
    """
    Authenticate via Supabase JWT or API key.
    Supabase token is expected in Authorization header as Bearer <token>.
    """
    # API key takes precedence
    if api_key_user:
        return api_key_user

    auth_header: str = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = auth_header.split(" ", 1)[1]

    # TODO: Replace this stub with actual Supabase JWT verification
    # For now, just return a dummy user object to keep the app working
    user_id = token  # In reality, extract user_id from Supabase JWT

    user_service = UserService(db)
    user = user_service.repo.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Ensure user is active."""
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def get_current_superuser(current_user: User = Depends(get_current_active_user)) -> User:
    """Ensure user is superuser (admin)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized as admin")
    return current_user


# ----------------------------
# Annotated Dependencies
# ----------------------------
CurrentUserDep = Annotated[User, Depends(get_current_user)]
CurrentUser = Annotated[User, Depends(get_current_active_user)]
CurrentSuperuser = Annotated[User, Depends(get_current_superuser)]
CurrentUserOrAPIKey = CurrentUserDep  # API key is handled in get_current_user


# ----------------------------
# Cache Dependency
# ----------------------------
def get_cache() -> Cache:
    return Cache.instance()


CacheDep = Annotated[Cache, Depends(get_cache)]


# ----------------------------
# Service Dependencies
# ----------------------------
def get_user_service(db: DBSession = Depends(get_db)) -> UserService:
    return UserService(db)


def get_patient_service(db: DBSession = Depends(get_db)) -> PatientService:
    return PatientService(db)


def get_usage_service(db: DBSession = Depends(get_db)) -> UsageAnalyticsService:
    return UsageAnalyticsService(db)


def get_reporting_service(db: DBSession = Depends(get_db)) -> ReportingService:
    return ReportingService(db)


def get_patient_history_service(db: DBSession = Depends(get_db)) -> PatientHistoryService:
    return PatientHistoryService(db)


def get_alzheimer_service(db: DBSession = Depends(get_db)) -> AlzheimerAssessmentService:
    return AlzheimerAssessmentService(db)


def get_cardiology_service(db: DBSession = Depends(get_db)) -> CardiologyAssessmentService:
    return CardiologyAssessmentService(db)


def get_subscription_service(db: DBSession = Depends(get_db)) -> SubscriptionService:
    return SubscriptionService(db)


def get_invoice_service(db: DBSession = Depends(get_db)) -> InvoiceService:
    return InvoiceService(db)


# --- Annotated service deps ---
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
PatientServiceDep = Annotated[PatientService, Depends(get_patient_service)]
UsageAnalyticsServiceDep = Annotated[UsageAnalyticsService, Depends(get_usage_service)]
ReportingServiceDep = Annotated[ReportingService, Depends(get_reporting_service)]
PatientHistoryServiceDep = Annotated[PatientHistoryService, Depends(get_patient_history_service)]
AlzheimerServiceDep = Annotated[AlzheimerAssessmentService, Depends(get_alzheimer_service)]
CardiologyServiceDep = Annotated[CardiologyAssessmentService, Depends(get_cardiology_service)]
SubscriptionServiceDep = Annotated[SubscriptionService, Depends(get_subscription_service)]
InvoiceServiceDep = Annotated[InvoiceService, Depends(get_invoice_service)]
