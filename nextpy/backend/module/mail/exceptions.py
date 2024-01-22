class EmailError(Exception):
    """Base class for email errors."""

class EmailConfigError(EmailError):
    """Raised for configuration related errors."""

class EmailSendError(EmailError):
    """Raised when sending an email fails."""
