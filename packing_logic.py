"""Legacy packing algorithm.

The calculation sequence is intentionally preserved during refactoring.
"""

from dataclasses import dataclass

from app.constants import MAX_BOX_WEIGHT
from models import BOXES, Box, Roll

EXCLUDED_BOX_DIMS = {(400, 200, 320), (200, 200, 220)}

# Full-box capacity matrix keyed by box dimensions and roll size.
PACKING_MATRIX = {
    (300, 300, 220): {
        (20, 300): 200,
        (20, 450): 160,
        (20, 600): 120,
        (44, 300): 100,
        (44, 450): 80,
        (45, 300): 100,
        (45, 450): 80,
        (50, 300): 80,
        (50, 450): 64,
        (55, 300): 80,
        (55, 450): 64,
        (55, 600): 48,
        (56, 300): 80,
        (56, 450): 64,
        (70, 300): 60,
        (70, 450): 48,
        (75, 300): 60,
        (75, 450): 48,
        (90, 300): 40,
        (90, 450): 32,
        (90, 600): 24,
        (95, 300): 40,
        (95, 450): 32,
        (95, 600): 24,
        (100, 300): 40,
        (100, 450): 32,
        (100, 600): 24,
        (104, 300): 40,
        (104, 450): 32,
        (104, 600): 24,
        (110, 300): 40,
        (110, 450): 32,
        (110, 600): 24,
        (220, 300): 20,
        (220, 450): 16,
    },
    (300, 300, 255): {
        (25, 300): 200,
        (25, 450): 160,
        (25, 600): 120,
        (30, 300): 160,
        (30, 450): 128,
        (30, 600): 96,
        (32, 300): 140,
        (32, 450): 112,
        (32, 600): 84,
        (33, 300): 140,
        (33, 450): 112,
        (33, 600): 84,
        (35, 300): 140,
        (35, 450): 112,
        (35, 500): 91,
        (35, 600): 84,
        (40, 300): 120,
        (40, 450): 96,
        (60, 300): 80,
        (60, 450): 64,
        (64, 300): 80,
        (64, 450): 64,
        (75, 600): 36,
        (80, 300): 60,
        (80, 450): 48,
        (80, 600): 36,
        (84, 300): 60,
        (84, 450): 48,
        (84, 600): 36,
        (120, 300): 40,
        (120, 450): 32,
    },
    (300, 300, 315): {
        (150, 300): 40,
        (150, 450): 32,
        (260, 300): 20,
        (260, 450): 16,
    },
}

_BOX_WEIGHTS: dict[tuple[int, int, int], float] = {
    (width, length, height): weight for width, length, height, weight in BOXES
}


@dataclass(slots=True, frozen=True)
class _PackingPlan:
    score: tuple[int, int, int, float, int]
    full_box: Box
    full_capacity: int
    full_count: int
    remaining: int
    partial_box: Box | None


def _build_box(box_dims: tuple[int, int, int]) -> Box:
    width, length, height = box_dims
    return Box(width, length, height, _BOX_WEIGHTS.get(box_dims, 0.0))


def _weight_limited_capacity(box: Box, roll: Roll) -> int:
    roll_weight = roll.weight()
    available_weight = MAX_BOX_WEIGHT - box.weight
    if roll_weight <= 0 or available_weight <= 0:
        return 0
    return int(available_weight // roll_weight)


def _geometric_capacity(box: Box, roll: Roll) -> int:
    diameter = roll.diameter_mm
    if diameter <= 0 or roll.width_mm <= 0:
        return 0

    cols = int(box.width // diameter)
    rows = int(box.length // diameter)
    layers = int(box.height // roll.width_mm)
    return cols * rows * layers


def _max_rolls_for_box(box: Box, roll: Roll) -> int:
    return max(
        0,
        min(_geometric_capacity(box, roll), _weight_limited_capacity(box, roll)),
    )


def _matrix_candidates(roll: Roll) -> list[tuple[Box, int]]:
    roll_key = (int(round(roll.width_mm)), int(round(roll.length_m)))
    candidates = []

    for box_dims, rules in PACKING_MATRIX.items():
        if box_dims in EXCLUDED_BOX_DIMS:
            continue

        per_box = rules.get(roll_key)
        if not per_box:
            continue

        box = _build_box(box_dims)
        per_box = min(per_box, _weight_limited_capacity(box, roll))
        if per_box > 0:
            candidates.append((box, per_box))

    return candidates


def _fallback_candidates(roll: Roll) -> list[tuple[Box, int]]:
    candidates = []
    for width, length, height, weight in BOXES:
        if (width, length, height) in EXCLUDED_BOX_DIMS:
            continue

        box = Box(width, length, height, weight)
        capacity = _max_rolls_for_box(box, roll)
        if capacity > 0:
            candidates.append((box, capacity))
    return candidates


def _single_box_candidates(roll: Roll) -> list[tuple[Box, int]]:
    """
    Candidates for packing one (possibly non-full) box.
    Matrix capacities override geometric capacities for the same box dimensions.
    """
    candidates = {}

    for box, capacity in _fallback_candidates(roll):
        key = (box.width, box.length, box.height)
        candidates[key] = (box, capacity)

    for box, capacity in _matrix_candidates(roll):
        key = (box.width, box.length, box.height)
        current = candidates.get(key)
        if current is None or capacity > current[1]:
            candidates[key] = (box, capacity)

    return list(candidates.values())


def _best_fitting_box(
    candidates: list[tuple[Box, int]],
    required_count: int,
) -> tuple[Box, int] | None:
    fitting = [item for item in candidates if item[1] >= required_count]
    if not fitting:
        return None
    return min(
        fitting,
        key=lambda item: (item[1] - required_count, item[0].volume(), item[0].weight),
    )


def _best_plan_min_free_space(
    total_quantity: int,
    full_candidates: list[tuple[Box, int]],
    one_box_candidates: list[tuple[Box, int]],
) -> _PackingPlan | None:
    best_plan = None

    for full_box, full_capacity in full_candidates:
        max_full_boxes = total_quantity // full_capacity

        for full_count in range(max_full_boxes, -1, -1):
            remaining = total_quantity - full_count * full_capacity

            if remaining == 0:
                free_space = 0
                partial_box = None
            else:
                fitting = _best_fitting_box(one_box_candidates, remaining)
                if not fitting:
                    continue
                partial_box, partial_capacity = fitting
                free_space = partial_capacity - remaining

            total_boxes = full_count + (1 if remaining > 0 else 0)
            partial_volume = partial_box.volume() if partial_box else 0
            partial_weight = partial_box.weight if partial_box else 0.0
            total_volume = full_count * full_box.volume() + partial_volume
            total_tare_weight = full_count * full_box.weight + partial_weight

            score = (
                total_boxes,
                free_space,
                total_volume,
                total_tare_weight,
                -full_capacity,
            )

            if best_plan is None or score < best_plan.score:
                best_plan = _PackingPlan(
                    score=score,
                    full_box=full_box,
                    full_capacity=full_capacity,
                    full_count=full_count,
                    remaining=remaining,
                    partial_box=partial_box,
                )

    return best_plan


def pack_rolls(roll: Roll, quantity: int) -> list[tuple[Box, int]]:
    """Pack rolls into boxes using the legacy optimization sequence."""
    boxes_used: list[tuple[Box, int]] = []
    remaining = int(quantity)

    if remaining <= 0:
        return boxes_used

    one_box_candidates = _single_box_candidates(roll)
    if not one_box_candidates:
        raise ValueError("Нет доступной коробки для данного типа рулона.")

    matrix_candidates = _matrix_candidates(roll)
    full_candidates = matrix_candidates if matrix_candidates else one_box_candidates
    best_plan = _best_plan_min_free_space(
        remaining, full_candidates, one_box_candidates
    )
    if not best_plan:
        raise ValueError(
            "Не удалось подобрать комбинацию упаковки для данного типа рулона."
        )

    if best_plan.full_count > 0:
        boxes_used.extend(
            [(best_plan.full_box, best_plan.full_capacity)] * best_plan.full_count
        )

    if best_plan.remaining > 0:
        partial_box = best_plan.partial_box
        if partial_box is None:
            raise ValueError("Не удалось подобрать коробку для остатка рулонов.")
        boxes_used.append((partial_box, best_plan.remaining))

    return boxes_used
