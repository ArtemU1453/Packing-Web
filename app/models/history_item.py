"""History item models."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class HistoryItem:
    """Single persisted calculation history record."""

    id: int | None
    created_at: datetime
    width_mm: float
    length_m: float
    quantity: int
    total_boxes: int
    total_weight: float
