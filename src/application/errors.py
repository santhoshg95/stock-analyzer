"""Exceptions raised at application boundaries."""


class PlatformError(Exception):
    """Base class for predictable platform errors."""


class ValidationError(PlatformError):
    """Raised when a caller supplies invalid input."""


class DataUnavailableError(PlatformError):
    """Raised when market data cannot be obtained."""


class AuthenticationError(PlatformError):
    """Raised when an external market-data session is not authenticated."""


class OrderError(PlatformError):
    """Raised when a paper order cannot be executed."""
