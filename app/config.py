"""Runtime configuration values."""

from dataclasses import dataclass
from pathlib import Path

from app.constants import DATABASE_FILE, LOG_FILE


@dataclass(slots=True, frozen=True)
class AppConfig:
    """Immutable application configuration."""

    database_path: Path = DATABASE_FILE
    log_path: Path = LOG_FILE
