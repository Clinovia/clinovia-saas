# backend/app/api/deps.py
"""
Dependency injection for FastAPI routes.

Includes:
- JWT-based authentication (current user, admin checks)
- API key authentication with usage tracking
- Database session injection (SQLAlchemy)
- Optional caching
- Service layer injection
"""

import logging
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import jwt, JWTError
from sqlalchemy.orm import Session as DBSession

from app.core.config import settings
from app.db.session import get_db
from app.db.models.users import User

# --- Optional imports for API key handling ---
try:
    from app.db.models.api_keys import APIKey as APIKeyModel
    from app.services.api_key_service import APIKeyService
except ImportError:
    APIKeyModel = None
    APIKeyService = None

# --- Service imports ---
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
# Auth Schemes
# ----------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# ----------------------------
# JWT Authentication
# ----------------------------
def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: DBSession = Depends(get_db),
) -> User:
    #Retrieve current user from JWT token.
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_service = UserService(db)
    user = user_service.repo.get(user_id)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Ensure user is active."""
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    #Ensure user is a superuser (admin).
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized as admin")
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive admin account")
    return current_user


# --- Annotated Auth Dependencies ---
CurrentUserDep = Annotated[User, Depends(get_current_user)]
CurrentUser = Annotated[User, Depends(get_current_active_user)]
CurrentSuperuser = Annotated[User, Depends(get_current_superuser)]

# ----------------------------
# Optional User (JWT optional)
# ----------------------------
def get_optional_current_user(
    db: DBSession = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme),
) -> Optional[User]:
    """Return user if token is valid, otherwise None."""
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        user_service = UserService(db)
        user = user_service.repo.get(user_id)
        return user if user and user.is_active else None
    except JWTError:
        return None


OptionalCurrentUser = Annotated[Optional[User], Depends(get_optional_current_user)]

# ----------------------------
# API Key Authentication (with tracking)
# ----------------------------
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

    # Track usage
    APIKeyService.increment_usage(db, db_key)
    return db_key.user


# ----------------------------
# Unified Auth (JWT or API key)
# ----------------------------
async def get_current_user_or_api_key(
    db: DBSession = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme),
    api_key_user: Optional[User] = Depends(get_api_key_user),
) -> User:
    """Allow authentication via JWT or API key."""
    if api_key_user:
        return api_key_user

    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: int = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token verification failed")

        user_service = UserService(db)
        user = user_service.repo.get(user_id)
        if user is None or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not active or not found")
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated: missing JWT token or API key",
        headers={"WWW-Authenticate": "Bearer"},
    )


CurrentUserOrAPIKey = Annotated[User, Depends(get_current_user_or_api_key)]

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


# --- Annotated versions ---
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
PatientServiceDep = Annotated[PatientService, Depends(get_patient_service)]
UsageAnalyticsServiceDep = Annotated[UsageAnalyticsService, Depends(get_usage_service)]
ReportingServiceDep = Annotated[ReportingService, Depends(get_reporting_service)]
PatientHistoryServiceDep = Annotated[PatientHistoryService, Depends(get_patient_history_service)]
AlzheimerServiceDep = Annotated[AlzheimerAssessmentService, Depends(get_alzheimer_service)]
CardiologyServiceDep = Annotated[CardiologyAssessmentService, Depends(get_cardiology_service)]
SubscriptionServiceDep = Annotated[SubscriptionService, Depends(get_subscription_service)]
InvoiceServiceDep = Annotated[InvoiceService, Depends(get_invoice_service)]

# --- Combined Billing Services ---
def get_billing_services(
    subscription: SubscriptionService = Depends(get_subscription_service),
    invoice: InvoiceService = Depends(get_invoice_service),
) -> dict:
    return {"subscription": subscription, "invoice": invoice}


BillingServiceDep = Annotated[dict, Depends(get_billing_services)]

# ----------------------------
# Exports
# ----------------------------
__all__ = [
    "get_db", "DBSession",
    # Auth
    "get_current_user", "get_current_active_user", "get_current_superuser",
    "CurrentUserDep", "CurrentUser", "CurrentSuperuser",
    "get_optional_current_user", "OptionalCurrentUser",
    "get_api_key_user", "get_current_user_or_api_key", "CurrentUserOrAPIKey",
    # Cache
    "get_cache", "CacheDep",
    # Services
    "UserServiceDep", "PatientServiceDep",
    "UsageAnalyticsServiceDep", "ReportingServiceDep",
    "PatientHistoryServiceDep", "AlzheimerServiceDep", "CardiologyServiceDep",
    "SubscriptionServiceDep", "InvoiceServiceDep", "BillingServiceDep",
]
