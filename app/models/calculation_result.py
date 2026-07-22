"""Calculation result models."""

from dataclasses import dataclass

from models import Box


@dataclass(slots=True, frozen=True)
class PackedBox:
    """Single packed box line in calculation output."""

    box: Box
    roll_count: int
    gross_weight: float


@dataclass(slots=True, frozen=True)
class CalculationResult:
    """Typed calculation result returned by calculation services."""

    width_mm: float
    length_m: float
    quantity: int
    boxes: tuple[PackedBox, ...]
    total_weight: float

    @property
    def total_boxes(self) -> int:
        """Return total number of boxes."""
        return len(self.boxes)

    @property
    def total_rolls(self) -> int:
        """Return total number of rolls."""
        return sum(item.roll_count for item in self.boxes)
