"""
User Utilities

Contains helper functions for authentication, password hashing,
validation, and other reusable utilities.
"""

import hashlib

from app.schemas.models import UserModel


def hash_password(password: str) -> str:
    """Hash a password (simple SHA256, replace with bcrypt in production)."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


def validate_user_data(user: UserModel) -> bool:
    """Basic validation for user object."""
    return bool(user.username and user.email and user.id)
