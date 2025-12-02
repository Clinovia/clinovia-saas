# backend/app/core/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.core.config import settings

# ----------------------------
# Password hashing
# ----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # Bcrypt only uses the first 72 bytes; truncate to be explicit and avoid errors
    password_bytes = password.encode("utf-8")[:72]
    return pwd_context.hash(password_bytes)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    plain_bytes = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(plain_bytes, hashed_password)


# ----------------------------
# JWT Token Management
# ----------------------------
def create_access_token(
    subject: str | int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: User ID or identifier to encode in token
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Subject (user_id) from token, or None if invalid
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        return user_id
    except JWTError:
        return None


# ----------------------------
# FastAPI Security Dependencies
# ----------------------------
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """
    Dependency to get current authenticated user.
    
    Validates JWT token and returns user object.
    Raises 401 if token is missing or invalid.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    user_id = decode_access_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Import here to avoid circular imports
    from app.db.models.users import User as user_crud
    from app.api.deps import get_db
    from fastapi import Request
    
    # Note: We need database session here
    # This is a simplified version - you may need to adjust based on your setup
    # For now, returning user_id wrapped in a simple object
    
    class UserAuth:
        def __init__(self, user_id: str):
            self.id = user_id
            self.is_active = True
            self.is_superuser = False  # Will be set from DB
    
    return UserAuth(user_id)


async def get_current_active_user(
    current_user = Depends(get_current_user)
):
    """
    Dependency to get current active user.
    
    Raises 400 if user is inactive.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_current_active_superuser(
    current_user = Depends(get_current_active_user)
):
    """
    Dependency to get current active superuser.
    
    Raises 403 if user is not a superuser/admin.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


# Alias for backward compatibility
async def require_admin(
    current_user = Depends(get_current_active_superuser)
):
    """
    Dependency that ensures the current user is an active superuser.
    
    This is an alias for get_current_active_superuser for better naming.
    Raises 401 if not authenticated, 403 if not admin.
    """
    return current_user


# ----------------------------
# Rate Limiting (In-Memory)
# ----------------------------
class RateLimiter:
    """
    Simple in-memory rate limiter.
    
    Note: Replace with Redis in production for distributed systems.
    """
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(
        self, 
        client_ip: str, 
        limit: int = 100, 
        window: int = 3600
    ) -> bool:
        """
        Check if request is allowed based on rate limit.
        
        Args:
            client_ip: Client IP address
            limit: Maximum requests allowed in window
            window: Time window in seconds
        
        Returns:
            True if allowed, False if rate limit exceeded
        """
        import time
        now = time.time()
        
        # Initialize if first request from this IP
        self.requests.setdefault(client_ip, [])
        
        # Keep only requests within the window
        self.requests[client_ip] = [
            t for t in self.requests[client_ip] 
            if t > now - window
        ]
        
        # Check if under limit
        if len(self.requests[client_ip]) < limit:
            self.requests[client_ip].append(now)
            return True
        
        return False
    
    def reset(self, client_ip: str):
        """Reset rate limit for a specific IP"""
        self.requests.pop(client_ip, None)
    
    def get_remaining(self, client_ip: str, limit: int = 100) -> int:
        """Get remaining requests for client"""
        current_requests = len(self.requests.get(client_ip, []))
        return max(0, limit - current_requests)


# Global rate limiter instance
rate_limiter = RateLimiter()


# ----------------------------
# Rate Limit Dependency
# ----------------------------
async def verify_rate_limit(request):
    """
    FastAPI dependency to enforce rate limit per client IP.
    
    Raises 429 if rate limit exceeded.
    """
    client_ip = request.client.host
    
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )
    
    return client_ip