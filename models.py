from dataclasses import dataclass

CORE_WEIGHT_100MM = 0.026  # kg
MATERIAL_WEIGHT_M2 = 0.009  # kg
DEFAULT_ROLL_DIAMETER_MM = 85

ROLL_DIAMETERS = {
    300: 64,
    450: 74,
    600: 85,
}

BOXES = [
    (260, 195, 110, 0.1),
    (260, 195, 245, 0.2),
    (300, 300, 220, 0.2),
    (300, 300, 255, 0.3),
    (300, 300, 315, 0.3),
]

@dataclass
class Roll:
    width_mm: float
    length_m: float

    @property
    def diameter_mm(self):
        rounded_length = int(round(self.length_m))
        return ROLL_DIAMETERS.get(rounded_length, DEFAULT_ROLL_DIAMETER_MM)

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
