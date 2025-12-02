# app/db/repositories/user_repository.py
from app.db.repositories.base_repository import BaseRepository
from app.db.models.users import User
from sqlalchemy.orm import Session

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    # Optional custom methods
    def get_by_email(self, email: str):
        return self.db.query(self.model).filter_by(email=email).first()

    def count_active(self) -> int:
        """Count users who are active"""
        # Assuming your User model has an 'is_active' field
        return self.db.query(self.model).filter(self.model.is_active == True).count()

    def disable_user(self, user_id: int) -> bool:
        """Disable a user account"""
        user = self.db.query(self.model).filter_by(id=user_id).first()
        if not user or not getattr(user, "is_active", False):
            return False
        user.is_active = False
        self.db.commit()
        return True
    
    def list_all(self):
        return self.db.query(self.model).all()
