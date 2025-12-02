# backend/app/core/logging.py
import logging
import sys

from app.core.config import settings
from pythonjsonlogger import jsonlogger


class SafeJsonFormatter(jsonlogger.JsonFormatter):
    """Ensures sensitive fields are NEVER logged"""

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        # Never log raw input data, patient info, or model inputs
        # Only log metadata: user_id, prediction_id, model_name


def setup_logger(name: str = "clinovia") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Already set up

    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = SafeJsonFormatter(
        "%(asctime)s %(level)s %(logger)s %(message)s",
        rename_fields={"asctime": "timestamp"},
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


# Global logger instance
logger = setup_logger()
