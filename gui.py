"""Compatibility helpers for the desktop GUI module.

The production UI lives in :mod:`app.ui.main_window`. This module is kept to
avoid delete/modify merge conflicts and to provide a stable import location for
external scripts that still import ``gui``.
"""

from app.config import AppConfig
from app.database.repository import HistoryRepository
from app.database.sqlite_manager import SQLiteManager
from app.services.calculation_service import CalculationService
from app.services.export_service import ExportService
from app.services.history_service import HistoryService


def create_main_window() -> object:
    """Create the configured PySide6 main window lazily."""
    from app.services.settings_service import SettingsService
    from app.ui.main_window import MainWindow

    config = AppConfig()
    sqlite_manager = SQLiteManager(config.database_path)
    sqlite_manager.initialize()
    return MainWindow(
        calculation_service=CalculationService(),
        history_service=HistoryService(HistoryRepository(sqlite_manager)),
        export_service=ExportService(),
        settings_service=SettingsService(),
    )
