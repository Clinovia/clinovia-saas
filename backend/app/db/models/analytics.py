from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .users import Base


class ApiUsageLog(Base):
    __tablename__ = "api_usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    endpoint = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status_code = Column(Integer)
