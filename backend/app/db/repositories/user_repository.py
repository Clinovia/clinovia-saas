from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.db.models.users import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = User

    # --- Fetch user by ID ---
    async def get(self, user_id: UUID) -> Optional[User]:
        result = await self.db.execute(select(self.model).where(self.model.id == user_id))
        return result.scalars().first()

    # --- Fetch user by email ---
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(self.model).where(self.model.email == email))
        return result.scalars().first()

    # --- Count active users ---
    async def count_active(self) -> int:
        result = await self.db.execute(select(self.model).where(self.model.is_active.is_(True)))
        return result.scalars().count()

    # --- Disable user ---
    async def disable_user(self, user_id: UUID) -> bool:
        user = await self.get(user_id)
        if not user or not user.is_active:
            return False
        user.is_active = False
        await self.db.commit()
        return True

    # --- List all users ---
    async def list_all(self) -> List[User]:
        result = await self.db.execute(select(self.model))
        return result.scalars().all()

    # --- Optional: List by role ---
    async def list_by_role(self, role: str) -> List[User]:
        result = await self.db.execute(select(self.model).where(self.model.role == role))
        return result.scalars().all()
