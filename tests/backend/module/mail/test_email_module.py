# test_email_module.py
from pathlib import Path
import aiosmtplib
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
import pytest_asyncio
from email.mime.multipart import MIMEMultipart

from nextpy.backend.module.mail.config import EmailConfig
from nextpy.backend.module.mail.email_template import EmailTemplateManager
from nextpy.backend.module.mail.sender import EmailSender
from nextpy.backend.module.mail.message import EmailMessage
from nextpy.backend.module.mail.exceptions import EmailSendError

# Fixture for Email Configuration
@pytest.fixture
def email_config():
    # Specify the directory where your test_template.html is located
    test_template_dir = Path(__file__).parent
    return EmailConfig(
        MAIL_SERVER="smtp.example.com",
        MAIL_PORT=587,
        MAIL_USERNAME="user@example.com",
        MAIL_PASSWORD="password",
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,
        MAIL_DEFAULT_SENDER="sender@example.com",
        MAIL_TEMPLATE_FOLDER=str(test_template_dir)  # Set the directory where test_template.html is located
    )

@pytest.fixture
def mock_template_manager():
    # Mock your EmailTemplateManager here if needed, or provide a real instance
    return MagicMock(spec=EmailTemplateManager)

# Fixture for Email Template Manager
@pytest.fixture
def email_template_manager(email_config):
    return EmailTemplateManager(email_config)

# Fixture for Email Sender
@pytest.fixture
def email_sender(email_config, email_template_manager):
    return EmailSender(email_config, email_template_manager)

# Test for Email Template Rendering
def test_template_rendering(email_template_manager):
    rendered_content = email_template_manager.render_template("test_template.html", {"name": "Test"})
    assert "Test" in rendered_content

# Test for Sending Email
@pytest.mark.asyncio
async def test_send_email(email_config, mock_template_manager):
    # Mock the SMTP client
    with patch('aiosmtplib.SMTP') as mock_smtp:
        mock_smtp.return_value.connect = AsyncMock()

        email_sender = EmailSender(email_config, mock_template_manager)

        # Mock the connect, starttls, login, send_message and quit methods
        mock_smtp.return_value.connect = AsyncMock()
        mock_smtp.return_value.starttls = AsyncMock()
        mock_smtp.return_value.login = AsyncMock()
        mock_smtp.return_value.send_message = AsyncMock()
        mock_smtp.return_value.quit = AsyncMock()

        # Properly instantiate EmailMessage
        message = EmailMessage(
            recipients=["recipient@example.com"],
            subject="Test Subject",
            body="Test email body"
        )
        await email_sender.send_email(message)

        # Assertions to ensure methods were called
        mock_smtp.return_value.connect.assert_called_once()
        mock_smtp.return_value.starttls.assert_called_once()
        mock_smtp.return_value.login.assert_called_once()
        mock_smtp.return_value.send_message.assert_called_once()
        mock_smtp.return_value.quit.assert_called_once()


# Test for Handling Email Sending Failure
@pytest.mark.asyncio
async def test_send_email_failure(email_config, mock_template_manager):
    # Mock the SMTP client
    with patch('aiosmtplib.SMTP') as mock_smtp:
        mock_smtp.return_value.connect = AsyncMock(side_effect=aiosmtplib.errors.SMTPConnectError("Connection error"))
        mock_smtp.return_value.is_connected = True
        mock_smtp.return_value.quit = AsyncMock()

        email_sender = EmailSender(email_config, mock_template_manager)

        # Properly instantiate EmailMessage
        message = EmailMessage(
            recipients=["recipient@example.com"],
            subject="Test Email",
            body="This is a test email."
        )
        email_sender.config.MAIL_SERVER = "invalid.server.com"  # Intentionally incorrect

        with pytest.raises(EmailSendError):
            await email_sender.send_email(message)
