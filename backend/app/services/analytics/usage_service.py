"""
Tracks and stores API usage statistics.
"""

from datetime import datetime
from typing import Dict, List


class UsageAnalyticsService:
    def __init__(self):
        self._usage_log: List[Dict] = []

    def record_event(self, user_id: str, endpoint: str, status: str):
        """Record a usage event for analytics."""
        event = {
            "user_id": user_id,
            "endpoint": endpoint,
            "status": status,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._usage_log.append(event)

    def get_usage_summary(self, user_id: str) -> dict:
        """Return aggregated usage stats per user."""
        user_events = [e for e in self._usage_log if e["user_id"] == user_id]
        return {
            "user_id": user_id,
            "total_calls": len(user_events),
            "successful_calls": sum(e["status"] == "success" for e in user_events),
        }
