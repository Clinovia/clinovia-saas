"""
Dependency injection for FastAPI routes (Supabase-compatible).

- Supabase is the source of truth for identity
- JWTs are verified via ES256 + JWKS
- Local users table is automatically synced (UID + Email)
"""

import logging
import json
import base64
from dataclasses import dataclass
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session as DBSession
import httpx
from authlib.jose import JsonWebKey, jwt as authlib_jwt

from app.db.session import get_db

# Services
from app.services.cache import Cache
from app.services.users.user_service import UserService
from app.services.patients.patient_service import PatientService
from app.services.assessments.patient_history_service import PatientHistoryService

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
# Supabase authentication with DB sync
# -------------------------------------------------------
async def get_current_user(
    request: Request,
    db: DBSession = Depends(get_db),
) -> AuthenticatedUser:

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = auth_header.split(" ", 1)[1]
    payload = await verify_supabase_jwt(token)

    # Supabase user ID (source of truth)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Supabase token",
        )

    email = payload.get("email")

    # ---------------------------
    # Sync with local users table
    # ---------------------------
    from app.db.models.users import User as UserModel

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        user = UserModel(id=user_id, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Inserted new user {user_id} ({email}) into local users table")

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

def get_patient_history_service(db: DBSession = Depends(get_db)) -> PatientHistoryService:
    return PatientHistoryService(db)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
PatientServiceDep = Annotated[PatientService, Depends(get_patient_service)]
PatientHistoryServiceDep = Annotated[PatientHistoryService, Depends(get_patient_history_service)]
