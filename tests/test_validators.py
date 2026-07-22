"""Tests for input validators."""

import pytest

from app.exceptions import ValidationError
from app.utils.validators import parse_decimal, parse_quantity


def test_parse_decimal_accepts_comma() -> None:
    """Decimal parser accepts locale comma separator."""
    assert parse_decimal("55,5", "Ширина") == 55.5


def test_parse_quantity_accepts_positive_integer() -> None:
    """Quantity parser accepts positive integers."""
    assert parse_quantity("128") == 128


@pytest.mark.parametrize("value", ["", "0", "-1", "abc"])
def test_parse_quantity_rejects_invalid(value: str) -> None:
    """Quantity parser rejects empty, non-positive, and text values."""
    with pytest.raises(ValidationError):
        parse_quantity(value)
