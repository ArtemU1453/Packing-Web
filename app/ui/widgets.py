"""Reusable UI widgets."""

from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit


class FieldEdit(QLineEdit):
    """Single-line input with a stable semantic name."""

    def __init__(self, placeholder: str) -> None:
        super().__init__()
        self.setPlaceholderText(placeholder)


class ReportView(QTextEdit):
    """Read-only report text view."""

    def __init__(self) -> None:
        super().__init__()
        self.setReadOnly(True)


class MutedLabel(QLabel):
    """Label styled as secondary explanatory text."""

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setWordWrap(True)
        self.setObjectName("mutedLabel")
