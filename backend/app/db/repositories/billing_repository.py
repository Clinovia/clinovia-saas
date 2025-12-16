from app.db.models.billing import Subscription
from uuid import UUID

from .base_repository import BaseRepository


class BillingRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(Subscription, db)

    def get_active_subscription(self, user_id: UUID):
        return (
            self.db.query(self.model)
            .filter(self.model.user_id == user_id)
            .filter(self.model.status == "active")
            .first()
        )
