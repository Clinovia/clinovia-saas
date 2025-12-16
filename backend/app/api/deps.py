# backend/app/api/deps.py

"""
Dependency injection for FastAPI routes (Supabase-compatible).

- Supabase is the source of truth for identity
- JWTs are verified via ES256 + JWKS
- Local users table is automatically synced (UID + Email)
- API key auth preserved
"""

import logging
import json
import base64
from dataclasses import dataclass
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session as DBSession
import httpx
from authlib.jose import JsonWebKey, jwt as authlib_jwt

from app.db.session import get_db

# Optional API key modules
try:
    from app.db.models.api_keys import APIKey as APIKeyModel
    from app.services.api_key_service import APIKeyService
except ImportError:
    APIKeyModel = None
    APIKeyService = None

# Services
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

# -------------------------------------------------------
# Supabase JWT configuration
# -------------------------------------------------------
SUPABASE_JWKS_URL = "https://cprwuuuvwaqttztaklam.supabase.co/auth/v1/.well-known/jwks.json"

_JWK_SET: Optional[dict] = None

# -------------------------------------------------------
# Auth context
# -------------------------------------------------------
@dataclass
class AuthenticatedUser:
    id: str
    email: Optional[str] = None

# -------------------------------------------------------
# JWKS utilities
# -------------------------------------------------------
async def fetch_jwks() -> dict:
    global _JWK_SET
    if _JWK_SET is not None:
        return _JWK_SET

    async with httpx.AsyncClient() as client:
        resp = await client.get(SUPABASE_JWKS_URL, timeout=5)
        resp.raise_for_status()
        _JWK_SET = resp.json()
        return _JWK_SET

async def verify_supabase_jwt(token: str) -> dict:
    try:
        header_b64 = token.split(".")[0]
        header_b64 += "=" * (-len(header_b64) % 4)
        header = json.loads(base64.urlsafe_b64decode(header_b64))

        kid = header.get("kid")
        jwks = await fetch_jwks()
        key_data = next((k for k in jwks["keys"] if k.get("kid") == kid), None)

        if not key_data:
            raise ValueError("Matching JWK not found")

        key = JsonWebKey.import_key(key_data)
        claims = authlib_jwt.decode(token, key)
        claims.validate()
        return dict(claims)

    except Exception as e:
        logger.error("JWT verification failed", exc_info=e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

# -------------------------------------------------------
# API key authentication (optional)
# -------------------------------------------------------
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key_user(
    db: DBSession = Depends(get_db),
    key: Optional[str] = Depends(api_key_header),
) -> Optional[AuthenticatedUser]:
    if not key or APIKeyService is None:
        return None

    db_key = APIKeyService.get_key_by_value(db, key)
    if not db_key or not db_key.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or inactive API key",
        )

    APIKeyService.increment_usage(db, db_key)

    return AuthenticatedUser(
        id=str(db_key.user_id),
        email=None,
    )

# -------------------------------------------------------
# Supabase authentication with DB sync
# -------------------------------------------------------
async def get_current_user(
    request: Request,
    db: DBSession = Depends(get_db),
    api_key_user: Optional[AuthenticatedUser] = Depends(get_api_key_user),
) -> AuthenticatedUser:
    if api_key_user:
        return api_key_user

    auth_header = request.headers.get("Authorization", "")
    print("🔍 Auth header:", auth_header)  # ← ADD THIS
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = auth_header.split(" ", 1)[1]
    payload = await verify_supabase_jwt(token)

    # Supabase payload keys are UID and Email (case-sensitive)
    user_id = payload.get("UID") or payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Supabase token",
        )

    email = payload.get("Email") or payload.get("email")

    # ---------------------------
    # Sync with local users table
    # ---------------------------
    from app.db.models.users import User as UserModel

    # In get_current_user or wherever you create the user
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        # Only generate a new ID if truly creating a new user
        user = UserModel(id=user_id, email=email)  # ideally user_id == Supabase 'sub'
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Inserted new user {user_id} ({email}) into local users table")
    else:
        # Optional: update ID if it changed (shouldn't happen if using Supabase 'sub')
        if user.id != user_id:
            logger.warning(f"User email {email} exists with ID {user.id}, but token has ID {user_id}")
            # Decide: keep old ID? update to new? (usually keep Supabase 'sub' as source of truth)

    return AuthenticatedUser(
        id=user_id,
        email=email,
    )

# -------------------------------------------------------
# Annotated dependencies
# -------------------------------------------------------
CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]

# -------------------------------------------------------
# Cache dependency
# -------------------------------------------------------
def get_cache() -> Cache:
    return Cache.instance()

CacheDep = Annotated[Cache, Depends(get_cache)]

# -------------------------------------------------------
# Service dependencies
# -------------------------------------------------------
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

# Annotated service dependencies
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
PatientServiceDep = Annotated[PatientService, Depends(get_patient_service)]
UsageAnalyticsServiceDep = Annotated[UsageAnalyticsService, Depends(get_usage_service)]
ReportingServiceDep = Annotated[ReportingService, Depends(get_reporting_service)]
PatientHistoryServiceDep = Annotated[PatientHistoryService, Depends(get_patient_history_service)]
AlzheimerServiceDep = Annotated[AlzheimerAssessmentService, Depends(get_alzheimer_service)]
CardiologyServiceDep = Annotated[CardiologyAssessmentService, Depends(get_cardiology_service)]
SubscriptionServiceDep = Annotated[SubscriptionService, Depends(get_subscription_service)]
InvoiceServiceDep = Annotated[InvoiceService, Depends(get_invoice_service)]
