from uuid import UUID
from app.db.models.analytics import ApiUsageLog

from .base_repository import BaseRepository


class AnalyticsRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(ApiUsageLog, db)

    def log_usage(self, user_id: UUID, endpoint: str, status_code: int):
        return self.create(
            {"user_id": user_id, "endpoint": endpoint, "status_code": status_code}
        )
