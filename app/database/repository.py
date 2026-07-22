"""Repository layer for application persistence."""

from datetime import datetime
from sqlite3 import Row

from app.database.sqlite_manager import SQLiteManager
from app.models.history_item import HistoryItem


class HistoryRepository:
    """Encapsulates all SQL operations for calculation history."""

    def __init__(self, sqlite_manager: SQLiteManager) -> None:
        self._sqlite_manager = sqlite_manager

    def add(self, item: HistoryItem) -> HistoryItem:
        """Persist a history item and return it with generated id."""
        with self._sqlite_manager.connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO history (
                    created_at, width_mm, length_m, quantity,
                    total_boxes, total_weight
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    item.created_at.isoformat(),
                    item.width_mm,
                    item.length_m,
                    item.quantity,
                    item.total_boxes,
                    item.total_weight,
                ),
            )
            return HistoryItem(
                id=cursor.lastrowid,
                created_at=item.created_at,
                width_mm=item.width_mm,
                length_m=item.length_m,
                quantity=item.quantity,
                total_boxes=item.total_boxes,
                total_weight=item.total_weight,
            )

    def list_recent(self, limit: int = 100) -> tuple[HistoryItem, ...]:
        """Return recent history records."""
        with self._sqlite_manager.connection() as connection:
            rows = connection.execute(
                """
                SELECT id, created_at, width_mm, length_m, quantity,
                       total_boxes, total_weight
                FROM history
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return tuple(self._row_to_item(row) for row in rows)

    @staticmethod
    def _row_to_item(row: Row) -> HistoryItem:
        """Convert SQLite row to domain model."""
        return HistoryItem(
            id=row["id"],
            created_at=datetime.fromisoformat(row["created_at"]),
            width_mm=row["width_mm"],
            length_m=row["length_m"],
            quantity=row["quantity"],
            total_boxes=row["total_boxes"],
            total_weight=row["total_weight"],
        )
