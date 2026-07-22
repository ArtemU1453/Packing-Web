"""Application dialogs."""

from PySide6.QtWidgets import QMessageBox, QWidget


def show_error(parent: QWidget, title: str, message: str) -> None:
    """Display an error dialog."""
    QMessageBox.critical(parent, title, message)


def show_info(parent: QWidget, title: str, message: str) -> None:
    """Display an information dialog."""
    QMessageBox.information(parent, title, message)
