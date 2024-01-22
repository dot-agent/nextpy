from pydantic import BaseModel, EmailStr


class EmailConfig(BaseModel):
    """Configuration class for the email module."""

    MAIL_SERVER: str  # SMTP server address
    MAIL_PORT: int  # SMTP server port
    MAIL_USERNAME: str  # SMTP username
    MAIL_PASSWORD: str  # SMTP password
    MAIL_USE_TLS: bool = False  # Whether to use TLS
    MAIL_USE_SSL: bool = False  # Whether to use SSL
    MAIL_DEFAULT_SENDER: EmailStr  # Default email sender
    MAIL_TEMPLATE_FOLDER: str = None  # Path to the email templates directory
    MAIL_MAX_EMAILS: int = None  # Maximum number of emails to send
    MAIL_SUPPRESS_SEND: bool = False  # Suppress sending emails for testing

    class Config:
        env_prefix = "EMAIL_"  # Prefix for environment variable configuration
