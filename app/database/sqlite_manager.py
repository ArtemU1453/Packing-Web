"""SQLite connection manager."""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from app.exceptions import DatabaseError


class SQLiteManager:
    """Owns SQLite connections and schema initialization."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path

    def initialize(self) -> None:
        """Create database schema when it does not exist."""
        with self.connection() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    width_mm REAL NOT NULL,
                    length_m REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    total_boxes INTEGER NOT NULL,
                    total_weight REAL NOT NULL
                )
                """)

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        """Yield a SQLite connection with row access enabled."""
        try:
            self._database_path.parent.mkdir(parents=True, exist_ok=True)
            connection = sqlite3.connect(self._database_path)
            connection.row_factory = sqlite3.Row
            yield connection
            connection.commit()
        except sqlite3.Error as exc:
            raise DatabaseError(str(exc)) from exc
        finally:
            if "connection" in locals():
                connection.close()
