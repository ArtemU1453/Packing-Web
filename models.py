"""Domain models and packing constants."""

from dataclasses import dataclass
from functools import cache

CORE_WEIGHT_100MM = 0.026  # kg
MATERIAL_WEIGHT_M2 = 0.009  # kg
DEFAULT_ROLL_DIAMETER_MM = 85

ROLL_DIAMETERS: dict[int, int] = {
    300: 64,
    450: 74,
    600: 85,
}

BOXES: list[tuple[int, int, int, float]] = [
    (260, 195, 110, 0.1),
    (260, 195, 245, 0.2),
    (300, 300, 220, 0.2),
    (300, 300, 255, 0.3),
    (300, 300, 315, 0.3),
]


@dataclass(slots=True, frozen=True)
class Roll:
    """Ribbon roll input parameters."""

    width_mm: float
    length_m: float

    @property
    def diameter_mm(self) -> int:
        """Return roll diameter selected by rounded winding length."""
        rounded_length = int(round(self.length_m))
        return _diameter_for_length(rounded_length)

    def weight(self) -> float:
        """Return gross roll weight using the legacy formula."""
        core_weight = CORE_WEIGHT_100MM * (self.width_mm / 100)
        width_m = self.width_mm / 1000
        area = width_m * self.length_m
        material_weight = area * MATERIAL_WEIGHT_M2
        return core_weight + material_weight


@dataclass(slots=True, frozen=True)
class Box:
    """Packing box dimensions and tare weight."""

    width: int
    length: int
    height: int
    weight: float

    def volume(self) -> int:
        """Return box volume in cubic millimeters."""
        return self.width * self.length * self.height


@cache
def _diameter_for_length(length_m: int) -> int:
    """Return configured diameter for length or default diameter."""
    return ROLL_DIAMETERS.get(length_m, DEFAULT_ROLL_DIAMETER_MM)
