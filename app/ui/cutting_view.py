"""Cutting preview placeholder view."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget


class CuttingView(QWidget):
    """Lightweight drawing surface for future packing previews."""

    def __init__(self) -> None:
        super().__init__()
        self._line_pen = QPen(QColor("#1A3457"), 1)
        self._text_pen = QPen(QColor("#7B91B7"), 1)
        self._font = QFont("Consolas", 9)
        self.setMinimumHeight(80)

    def paintEvent(self, event: object) -> None:
        """Paint cached grid and placeholder label."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        painter.setPen(self._line_pen)
        for x in range(0, self.width(), 24):
            painter.drawLine(x, 0, x, self.height())
        painter.setPen(self._text_pen)
        painter.setFont(self._font)
        painter.drawText(
            self.rect(), Qt.AlignmentFlag.AlignCenter, "Предпросмотр упаковки"
        )
        painter.end()
        super().paintEvent(event)
