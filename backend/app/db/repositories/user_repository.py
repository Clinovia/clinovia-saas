# backend/app/db/repositories/user_repository.py
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.repositories.base_repository import BaseRepository
from app.db.models.users import User


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    # --- Fetch user by email ---
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(self.model).where(self.model.email == email))
        return result.scalars().first()

    # --- Count active users ---
    async def count_active(self) -> int:
        result = await self.db.execute(select(self.model).where(self.model.is_active == True))
        return result.scalars().count()

    # --- Disable user ---
    async def disable_user(self, user_id: int) -> bool:
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
