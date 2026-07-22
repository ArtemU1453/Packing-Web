"""Calculation service layer."""

from app.exceptions import CalculationError
from app.models.calculation_result import CalculationResult, PackedBox
from app.utils.formatting import ceil_one_decimal
from app.utils.validators import parse_decimal, parse_quantity
from models import Roll
from packing_logic import pack_rolls


class CalculationService:
    """Coordinates validation and packing calculation."""

    def calculate(self, width: str, length: str, quantity: str) -> CalculationResult:
        """Validate raw UI values and calculate packing result."""
        width_mm = parse_decimal(width, "Ширина рулона")
        length_m = parse_decimal(length, "Намотка")
        qty = parse_quantity(quantity)
        return self.calculate_values(width_mm, length_m, qty)

    def calculate_values(
        self,
        width_mm: float,
        length_m: float,
        quantity: int,
    ) -> CalculationResult:
        """Calculate packing result from typed values."""
        roll = Roll(width_mm, length_m)
        try:
            packed = pack_rolls(roll, quantity)
        except ValueError as exc:
            raise CalculationError(str(exc)) from exc
        if not packed:
            raise CalculationError("Модуль упаковки вернул пустой результат.")
        boxes = tuple(
            PackedBox(box, count, ceil_one_decimal(count * roll.weight() + box.weight))
            for box, count in packed
        )
        total_weight = ceil_one_decimal(sum(item.gross_weight for item in boxes))
        return CalculationResult(width_mm, length_m, quantity, boxes, total_weight)
