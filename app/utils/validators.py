"""Input validators."""

from app.exceptions import ValidationError


def parse_decimal(value: str, field_name: str) -> float:
    """Parse a positive decimal number that may use comma as separator."""
    normalized = value.strip().replace(",", ".")
    try:
        parsed = float(normalized)
    except ValueError as exc:
        raise ValidationError(f"Поле «{field_name}» должно быть числом.") from exc
    if parsed <= 0:
        raise ValidationError(f"Поле «{field_name}» должно быть больше нуля.")
    return parsed


def parse_quantity(value: str) -> int:
    """Parse a positive integer quantity."""
    normalized = value.strip()
    try:
        quantity = int(normalized)
    except ValueError as exc:
        raise ValidationError("Поле «Количество» должно быть целым числом.") from exc
    if quantity <= 0:
        raise ValidationError("Поле «Количество» должно быть больше нуля.")
    return quantity
