from dataclasses import dataclass
import math

CORE_WEIGHT_100MM = 0.026  # кг
MATERIAL_WEIGHT_M2 = 0.009  # кг

ROLL_DIAMETERS = {
    300: 64,
    450: 74,
    600: 85,
}

BOXES = [
    (260,195,110,0.1),
    (260,195,245,0.2),
    (300,300,220,0.2),
    (300,300,255,0.3),
    (300,300,315,0.3),
    (200,200,220,0.2),
    (400,200,320,0.3),
]

@dataclass
class Roll:
    width_mm: float
    length_m: float

    @property
    def diameter_mm(self):
        return ROLL_DIAMETERS.get(self.length_m, 85)

    def weight(self):
        core_weight = CORE_WEIGHT_100MM * (self.width_mm / 100)

        width_m = self.width_mm / 1000
        area = width_m * self.length_m
        material_weight = area * MATERIAL_WEIGHT_M2

        return core_weight + material_weight


@dataclass
class Box:
    width: int
    length: int
    height: int
    weight: float

    def volume(self):
        return self.width * self.length * self.height
