"""Logging configuration."""

import logging
from logging.handlers import RotatingFileHandler

from app.config import AppConfig
from app.constants import LOG_BACKUP_COUNT, LOG_MAX_BYTES


def configure_logging(config: AppConfig) -> None:
    """Configure application logging with rotation."""
    config.log_path.parent.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
    handler = RotatingFileHandler(
        config.log_path,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()
    root.addHandler(handler)
