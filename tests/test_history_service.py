"""Tests for history service and repository integration."""

from pathlib import Path

from app.database.repository import HistoryRepository
from app.database.sqlite_manager import SQLiteManager
from app.models.calculation_result import CalculationResult
from app.services.history_service import HistoryService


def test_history_service_records_result(tmp_path: Path) -> None:
    """History service stores and reads recent calculation results."""
    manager = SQLiteManager(tmp_path / "history.sqlite3")
    manager.initialize()
    service = HistoryService(HistoryRepository(manager))
    result = CalculationResult(55, 450, 128, (), 12.3)

    saved = service.record(result)
    recent = service.recent()

    assert saved.id is not None
    assert len(recent) == 1
    assert recent[0].quantity == 128
    assert recent[0].total_weight == 12.3
