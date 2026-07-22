"""Application exception hierarchy."""


class ApplicationError(Exception):
    """Base class for expected application errors."""


class ValidationError(ApplicationError):
    """Raised when user input is invalid."""


class DatabaseError(ApplicationError):
    """Raised when persistence operations fail."""


class CalculationError(ApplicationError):
    """Raised when packing calculation fails."""


class ExportError(ApplicationError):
    """Raised when export operation fails."""
