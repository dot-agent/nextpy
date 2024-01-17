"""The email package."""

from .config import EmailConfig
from .message import EmailMessage
from .sender import EmailSender
from .email_template import EmailTemplateManager
from .exceptions import EmailConfigError, EmailSendError

__all__ = [
    'EmailConfig',
    'EmailSender',
    'EmailMessage',
    'EmailTemplateManager',
    'EmailConfigError',
    'EmailSendError'
]
