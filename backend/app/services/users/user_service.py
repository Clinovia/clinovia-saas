# backend/app/services/users/user_service.py
from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.repositories.user_repository import UserRepository
from app.db.models.users import User
from app.schemas.users import UserCreate, UserRead, UserUpdate

class UserService:
    """Service layer for user CRUD operations (Supabase handles auth)."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def _to_response(self, user: User) -> UserRead:
        """Convert ORM User to UserRead schema."""
        return UserRead.model_validate(user)

    # -------------------
    # CRUD Operations
    # -------------------

    async def create(self, user_data: UserCreate) -> UserRead:
        """Create a new user (metadata only)."""
        existing_user = self.repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email is already in use")

        new_user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            is_active=True,
            is_superuser=False
        )

        user = self.repo.create(new_user)
        return self._to_response(user)

    async def get(self, user_id: int) -> Optional[UserRead]:
        user = self.repo.get(user_id)
        return self._to_response(user) if user else None

    async def get_by_email(self, email: str) -> Optional[UserRead]:
        user = self.repo.get_by_email(email)
        return self._to_response(user) if user else None

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[UserRead]:
        users = self.repo.list_all()[skip: skip + limit]
        return [self._to_response(u) for u in users]

    async def update(self, user_id: int, user_update: UserUpdate) -> UserRead:
        user = self.repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        updated_user = self.repo.update(user)
        return self._to_response(updated_user)

    async def delete(self, user_id: int) -> None:
        """Soft-delete / deactivate a user."""
        user = self.repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        user.is_active = False
        self.repo.update(user)
