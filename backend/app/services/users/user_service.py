"""
User service (Supabase-only)

Responsibilities:
- Interpret Supabase-authenticated user identity
- Provide normalized user info to the application
- NO local persistence
- NO CRUD
- NO SQLAlchemy

Supabase is the source of truth for users.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class UserContext:
    """
    Normalized user representation derived from Supabase JWT.
    """
    id: str
    email: Optional[str] = None
    role: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class UserService:
    """
    Supabase-only user service.

    This service does NOT:
    - create users
    - update users
    - delete users
    - store users locally

    Those responsibilities belong to Supabase.
    """

    @staticmethod
    def from_jwt_payload(payload: Dict[str, Any]) -> UserContext:
        """
        Build a UserContext from a verified Supabase JWT payload.
        """
        return UserContext(
            id=payload.get("sub"),
            email=payload.get("email"),
            role=payload.get("role") or payload.get("app_metadata", {}).get("role"),
            metadata=payload.get("user_metadata"),
        )

    @staticmethod
    def get_user_id(user: UserContext) -> str:
        return user.id

    @staticmethod
    def is_admin(user: UserContext) -> bool:
        """
        Admin check placeholder.

        Future:
        - Enforce via Supabase app_metadata / custom claims
        """
        return user.role == "admin"
