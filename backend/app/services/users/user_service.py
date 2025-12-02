from typing import Optional
from sqlalchemy.orm import Session
from app.db.repositories.user_repository import UserRepository
from app.db.models.users import User
from app.schemas.auth import Token
from app.schemas.users import UserCreate, UserLogin, UserRead, UserUpdate
from app.core.security import get_password_hash, verify_password, create_access_token


class UserService:
    """Service layer for user CRUD and authentication operations."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def _to_response(self, user: User) -> UserRead:
        """Convert ORM User to UserRead schema."""
        return UserRead.model_validate(user)  # ✅ Prefer Pydantic's built-in conversion

    # -------------------
    # CRUD Operations
    # -------------------

    def create_user(self, user_data: UserCreate) -> UserRead:
        """Create a new active user."""
        existing_user = self.repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email is already in use")  # Updated message to match frontend

        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
        )

        user = self.repo.create(new_user)
        return self._to_response(user)

    def get_user_by_id(self, user_id: int) -> Optional[UserRead]:
        """Retrieve a user by ID."""
        user = self.repo.get(user_id)
        return self._to_response(user) if user else None

    def update_user(self, user_id: int, user_update: UserUpdate) -> UserRead:
        """Update user fields; handle password hashing if provided."""
        user = self.repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        # Only allow updating known fields (prevent arbitrary setattr)
        allowed_fields = {"email", "full_name", "is_active", "is_superuser", "hashed_password"}
        for field, value in update_data.items():
            if field in allowed_fields and hasattr(user, field):
                setattr(user, field, value)

        updated_user = self.repo.update(user)
        return self._to_response(updated_user)

    def deactivate_user(self, user_id: int) -> UserRead:
        """Soft-delete by deactivating the user."""
        user = self.repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        if not user.is_active:
            raise ValueError("User is already deactivated")

        user.is_active = False
        updated_user = self.repo.update(user)
        return self._to_response(updated_user)

    # -------------------
    # Authentication
    # -------------------

    def authenticate_and_create_token(self, credentials: UserLogin) -> Optional[Token]:
        """Authenticate user and return a JWT token if credentials are valid."""
        user = self.repo.get_by_email(credentials.email)
        if not user or not user.is_active:
            return None

        if not verify_password(credentials.password, user.hashed_password):
            return None

        access_token = create_access_token(subject=str(user.id))
        return Token(access_token=access_token, token_type="bearer")