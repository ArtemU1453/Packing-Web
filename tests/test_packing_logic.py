"""Tests for legacy packing calculations."""

import pytest

from models import Roll
from packing_logic import pack_rolls


@pytest.mark.parametrize(
    ("width", "length", "quantity", "expected_boxes", "expected_rolls"),
    [
        (55, 450, 128, 2, 128),
        (35, 500, 91, 1, 91),
        (260, 450, 17, 2, 17),
    ],
)
def test_pack_rolls_preserves_total_quantity(
    width: float,
    length: float,
    quantity: int,
    expected_boxes: int,
    expected_rolls: int,
) -> None:
    """Packing must preserve the total requested quantity."""
    result = pack_rolls(Roll(width, length), quantity)

    assert len(result) == expected_boxes
    assert sum(count for _, count in result) == expected_rolls


def test_pack_rolls_rejects_impossible_roll() -> None:
    """Oversized rolls must fail with the legacy ValueError contract."""
    with pytest.raises(ValueError):
        pack_rolls(Roll(1000, 450), 1)
