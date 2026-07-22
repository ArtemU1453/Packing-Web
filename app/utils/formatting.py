"""Formatting helpers for UI and exports."""

import math


def ceil_one_decimal(value: float) -> float:
    """Round value up to one decimal place without changing legacy behavior."""
    return math.ceil(value * 10) / 10


def format_dimensions(width: int, length: int, height: int) -> str:
    """Format box dimensions for display."""
    return f"{width}x{length}x{height}"


def format_weight(value: float) -> str:
    """Format kilogram value for display."""
    return f"{ceil_one_decimal(value):.1f} кг"
