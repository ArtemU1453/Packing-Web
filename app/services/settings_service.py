"""Settings service based on QSettings."""

from pathlib import Path

from PySide6.QtCore import QByteArray, QSettings

from app.constants import APP_NAME, ORGANIZATION_NAME, Theme


class SettingsService:
    """Typed wrapper around QSettings."""

    def __init__(self) -> None:
        self._settings = QSettings(ORGANIZATION_NAME, APP_NAME)

    def geometry(self) -> QByteArray | None:
        """Return saved window geometry."""
        value = self._settings.value("window/geometry")
        return value if isinstance(value, QByteArray) else None

    def set_geometry(self, value: QByteArray) -> None:
        """Persist window geometry."""
        self._settings.setValue("window/geometry", value)

    def theme(self) -> Theme:
        """Return selected theme."""
        value = self._settings.value("ui/theme", Theme.DARK.value)
        return Theme(str(value))

    def set_theme(self, theme: Theme) -> None:
        """Persist selected theme."""
        self._settings.setValue("ui/theme", theme.value)

    def last_folder(self) -> Path:
        """Return last used folder."""
        return Path(str(self._settings.value("files/last_folder", Path.cwd())))

    def set_last_folder(self, path: Path) -> None:
        """Persist last used folder."""
        self._settings.setValue("files/last_folder", str(path))

    def last_inputs(self) -> tuple[str, str, str]:
        """Return last calculation input values."""
        return (
            str(self._settings.value("inputs/width", "")),
            str(self._settings.value("inputs/length", "")),
            str(self._settings.value("inputs/quantity", "")),
        )

    def set_last_inputs(self, width: str, length: str, quantity: str) -> None:
        """Persist last calculation input values."""
        self._settings.setValue("inputs/width", width)
        self._settings.setValue("inputs/length", length)
        self._settings.setValue("inputs/quantity", quantity)
