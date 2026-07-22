"""Application constants."""

from enum import StrEnum
from pathlib import Path

APP_NAME = "Packing Calculator"
ORGANIZATION_NAME = "IndustrialPackingSystem"
WINDOW_TITLE = "Калькулятор упаковки риббона"
DEFAULT_WINDOW_WIDTH = 980
DEFAULT_WINDOW_HEIGHT = 640
MIN_WINDOW_WIDTH = 820
MIN_WINDOW_HEIGHT = 560
MAX_BOX_WEIGHT = 21.0
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"
LOG_MAX_BYTES = 10 * 1024 * 1024
LOG_BACKUP_COUNT = 5
DATABASE_FILE = Path("packing_history.sqlite3")
CSV_DELIMITER = ";"


class Theme(StrEnum):
    """Supported UI themes."""

    DARK = "dark"
