# Changelog

## Unreleased

### Created files
- `app/__init__.py` — application package marker.
- `app/main.py` — PySide6 application composition root.
- `app/constants.py` — shared constants and enums.
- `app/config.py` — immutable runtime configuration.
- `app/exceptions.py` — application exception hierarchy.
- `app/models/calculation_result.py` — typed calculation result dataclasses.
- `app/models/history_item.py` — typed history item dataclass.
- `app/services/calculation_service.py` — calculation orchestration service.
- `app/services/history_service.py` — calculation history use cases.
- `app/services/export_service.py` — CSV export service.
- `app/services/settings_service.py` — QSettings wrapper.
- `app/database/sqlite_manager.py` — SQLite connection/schema manager.
- `app/database/repository.py` — history repository with SQL encapsulation.
- `app/ui/main_window.py` — PySide6 main window.
- `app/ui/cutting_view.py` — cached painting preview widget.
- `app/ui/dialogs.py` — dialog helpers.
- `app/ui/widgets.py` — reusable UI widgets.
- `app/utils/validators.py` — input validation helpers.
- `app/utils/formatting.py` — display formatting helpers.
- `app/utils/logging.py` — RotatingFileHandler logging setup.
- `tests/test_packing_logic.py` — unit tests for calculation behavior.
- `tests/test_validators.py` — unit tests for validators.
- `tests/test_history_service.py` — unit tests for history service.
- `pyproject.toml` — tooling configuration.

### Changed files
- `main.py` — reduced to application startup delegation only.
- `models.py` — added slots dataclasses, type hints, docstrings, and cached diameter lookup.
- `packing_logic.py` — added type hints and an internal dataclass without changing calculation sequence.
- `requirements.txt` — added PySide6, test, formatting, linting, and type-checking tools.

### Deleted files
- None.

### New dependencies
- `PySide6` for the industrial desktop UI.
- `pytest` and `pytest-cov` for unit testing and coverage.
- `ruff`, `black`, `isort`, and `mypy` for code quality gates.

### Refactoring
- Introduced UI → Services → Repository → SQLite layering.
- Moved validation into dedicated validators.
- Added typed result models instead of dictionary-based service responses.
- Added application-specific exception hierarchy.
- Added rotating file logging to `logs/app.log`.
- Added QSettings-based settings service for geometry, theme, folder, and last inputs.
