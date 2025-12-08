# backend/app/core/security.py
from fastapi import HTTPException, status, Depends, Request
from app.db.session import get_db
from app.db.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users.user_service import UserService

# ----------------------------
# Role & Access Dependencies
# ----------------------------
async def get_current_active_user(user_id: str, db: AsyncSession = Depends(get_db)) -> User:
    """
    Fetch the current active user from the database.
    
    Args:
        user_id: Supabase user ID (passed from frontend)
        db: Database session
    
    Returns:
        User object
    """
    user_service = UserService(db)
    user = await user_service.get_by_supabase_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user or not found"
        )
    return user

async def get_current_active_superuser(user: User = Depends(get_current_active_user)) -> User:
    """
    Ensure the current user is a superuser/admin.
    """
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return user

# ----------------------------
# Optional: Simple Rate Limiter
# ----------------------------
class RateLimiter:
    """
    In-memory rate limiter.
    For production, consider Redis or another distributed store.
    """
    def __init__(self):
        self.requests = {}

    def is_allowed(self, client_ip: str, limit: int = 100, window: int = 3600) -> bool:
        import time
        now = time.time()
        self.requests.setdefault(client_ip, [])
        self.requests[client_ip] = [t for t in self.requests[client_ip] if t > now - window]

        if len(self.requests[client_ip]) < limit:
            self.requests[client_ip].append(now)
            return True
        return False

rate_limiter = RateLimiter()

async def verify_rate_limit(request: Request):
    """
    FastAPI dependency to enforce rate limit per client IP.
    Raises 429 if limit exceeded.
    """
    client_ip = request.client.host
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    return client_ip
