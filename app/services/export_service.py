"""Export service implementations."""

import csv
from pathlib import Path

from app.constants import CSV_DELIMITER
from app.exceptions import ExportError
from app.models.calculation_result import CalculationResult
from app.utils.formatting import format_dimensions


class ExportService:
    """Exports calculation results to files."""

    def export_csv(self, result: CalculationResult, path: Path) -> None:
        """Export calculation result to CSV."""
        try:
            with path.open("w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file, delimiter=CSV_DELIMITER)
                writer.writerow(["Коробка", "Рулонов", "Вес брутто"])
                for item in result.boxes:
                    box = item.box
                    writer.writerow(
                        [
                            format_dimensions(box.width, box.length, box.height),
                            item.roll_count,
                            f"{item.gross_weight:.1f}",
                        ]
                    )
                writer.writerow([])
                writer.writerow(["Итого коробок", result.total_boxes])
                writer.writerow(["Итого рулонов", result.total_rolls])
                writer.writerow(["Общий вес", f"{result.total_weight:.1f}"])
        except OSError as exc:
            raise ExportError(str(exc)) from exc
