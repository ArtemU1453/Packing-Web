"""History service layer."""

from datetime import datetime

from app.database.repository import HistoryRepository
from app.models.calculation_result import CalculationResult
from app.models.history_item import HistoryItem


class HistoryService:
    """Provides calculation history use cases."""

    def __init__(self, repository: HistoryRepository) -> None:
        self._repository = repository

    def record(self, result: CalculationResult) -> HistoryItem:
        """Store a calculation result in history."""
        item = HistoryItem(
            id=None,
            created_at=datetime.now().astimezone(),
            width_mm=result.width_mm,
            length_m=result.length_m,
            quantity=result.quantity,
            total_boxes=result.total_boxes,
            total_weight=result.total_weight,
        )
        return self._repository.add(item)

    def recent(self, limit: int = 100) -> tuple[HistoryItem, ...]:
        """Return recent calculation history."""
        return self._repository.list_recent(limit)
