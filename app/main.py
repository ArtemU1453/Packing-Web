"""Application composition root."""

import sys

from app.config import AppConfig
from app.database.repository import HistoryRepository
from app.database.sqlite_manager import SQLiteManager
from app.services.calculation_service import CalculationService
from app.services.export_service import ExportService
from app.services.history_service import HistoryService
from app.utils.logging import configure_logging


def main() -> None:
    """Start the desktop application."""
    from PySide6.QtWidgets import QApplication

    from app.services.settings_service import SettingsService
    from app.ui.main_window import MainWindow

    config = AppConfig()
    configure_logging(config)
    sqlite_manager = SQLiteManager(config.database_path)
    sqlite_manager.initialize()
    application = QApplication(sys.argv)
    window = MainWindow(
        calculation_service=CalculationService(),
        history_service=HistoryService(HistoryRepository(sqlite_manager)),
        export_service=ExportService(),
        settings_service=SettingsService(),
    )
    window.show()
    sys.exit(application.exec())
