"""
FastAPI dependency injection (Supabase-only, DB-optional)
"""

import logging
import json
import base64
import time
from dataclasses import dataclass
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request, status
from authlib.jose import JsonWebKey, jwt as authlib_jwt

from app.core.config import settings
from app.core import cache
from app.core.http import async_client

logger = logging.getLogger(__name__)

# -------------------------------------------------------
# Supabase JWT configuration
# -------------------------------------------------------

SUPABASE_URL = settings.SUPABASE_URL

if not SUPABASE_URL.startswith("http"):
    SUPABASE_URL = "https://" + SUPABASE_URL.lstrip("/")

SUPABASE_JWKS_URL = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"

JWKS_CACHE_KEY = "supabase_jwks"
JWKS_CACHE_TIME_KEY = "supabase_jwks_time"
JWKS_TTL = 600  # 10 minutes


# -------------------------------------------------------
# JWKS fetch with cache
# -------------------------------------------------------

async def get_jwks():

    cached_jwks = cache.get_cached_prediction(JWKS_CACHE_KEY)
    cached_time = cache.get_cached_prediction(JWKS_CACHE_TIME_KEY)

    now = time.time()

    if cached_jwks and cached_time and now - cached_time < JWKS_TTL:
        return cached_jwks

    resp = await async_client.get(SUPABASE_JWKS_URL)
    resp.raise_for_status()

    jwks = resp.json()

    cache.set_cached_prediction(JWKS_CACHE_KEY, jwks)
    cache.set_cached_prediction(JWKS_CACHE_TIME_KEY, now)

    logger.debug("Supabase JWKS refreshed")

    return jwks


# -------------------------------------------------------
# Auth context
# -------------------------------------------------------

@dataclass
class AuthenticatedUser:
    id: str
    email: Optional[str] = None


# -------------------------------------------------------
# Decode JWT header
# -------------------------------------------------------

def decode_jwt_header(token: str) -> dict:

    header_b64 = token.split(".")[0]
    padding = "=" * (-len(header_b64) % 4)

    return json.loads(
        base64.urlsafe_b64decode(header_b64 + padding)
    )


# -------------------------------------------------------
# JWT verification
# -------------------------------------------------------

async def verify_supabase_jwt(token: str) -> dict:

    try:

        header = decode_jwt_header(token)
        kid = header.get("kid")

        if not kid:
            raise ValueError("JWT header missing 'kid'")

        jwks = await get_jwks()

        key_data = next(
            (k for k in jwks.get("keys", []) if k.get("kid") == kid),
            None,
        )

        if not key_data:
            raise ValueError(f"No matching JWK for kid={kid}")

        key = JsonWebKey.import_key(key_data)

        claims = authlib_jwt.decode(token, key)
        claims.validate()

        return dict(claims)

    except HTTPException:
        raise

    except Exception as exc:

        logger.warning("JWT verification failed: %s", exc)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# -------------------------------------------------------
# Authentication dependency
# -------------------------------------------------------

async def get_current_user(request: Request) -> AuthenticatedUser:

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = auth_header.split(" ", 1)[1]

    payload = await verify_supabase_jwt(token)

    user_id = payload.get("sub")
    email = payload.get("email")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Supabase token",
        )

    return AuthenticatedUser(id=user_id, email=email)


# -------------------------------------------------------
# Annotated dependency
# -------------------------------------------------------

CurrentUser = Annotated[AuthenticatedUser, Depends(get_current_user)]