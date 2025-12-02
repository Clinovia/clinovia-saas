from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.models.api_keys import APIKey
from app.db.models.users import User


class APIKeyService:
    @staticmethod
    def create_api_key(db: Session, user: User) -> str:
        """Create and store a new API key for the user."""
        key = str(uuid4())
        db_key = APIKey(
            key=key,
            user_id=user.id,
            is_active=True,
            usage_count=0
        )
        db.add(db_key)
        db.commit()
        db.refresh(db_key)
        return key

    @staticmethod
    def get_user_keys(db: Session, user: User) -> List[APIKey]:
        """Get all active API keys for a user."""
        return db.query(APIKey).filter(
            APIKey.user_id == user.id,
            APIKey.is_active.is_(True)
        ).all()

    @staticmethod
    def get_key_by_value(db: Session, key: str) -> Optional[APIKey]:
        """Retrieve an API key by its value (for auth/usage)."""
        return db.query(APIKey).filter(
            APIKey.key == key,
            APIKey.is_active.is_(True)
        ).first()

    @staticmethod
    def revoke_key(db: Session, key_id: int, user: User) -> bool:
        """Revoke a key if it belongs to the user."""
        db_key = db.query(APIKey).filter(
            APIKey.id == key_id,
            APIKey.user_id == user.id
        ).first()
        
        if db_key and db_key.is_active:
            db_key.is_active = False
            db.commit()
            return True
        return False

    @staticmethod
    def increment_usage(db: Session, key: APIKey) -> None:
        """Increment usage count and update last_used_at."""
        key.usage_count += 1
        key.last_used_at = datetime.utcnow()
        db.commit()