from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base, TimestampMixin


class ApiUsageLog(Base, TimestampMixin):
    __tablename__ = "api_usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    endpoint = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
