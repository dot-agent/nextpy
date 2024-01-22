from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

import aiosmtplib

from .config import EmailConfig
from .email_template import EmailTemplateManager
from .exceptions import EmailSendError
from .message import EmailMessage


class EmailSender:
    def __init__(self, config: EmailConfig, template_manager: Optional[EmailTemplateManager] = None):
        self.config = config
        self.template_manager = template_manager

    async def send_email(self, message: EmailMessage, template_name: Optional[str] = None) -> None:
        """Sends an email message."""
        if self.config.MAIL_SUPPRESS_SEND:
            return

        smtp = aiosmtplib.SMTP()

        try:
            await smtp.connect(hostname=self.config.MAIL_SERVER, port=self.config.MAIL_PORT, use_tls=self.config.MAIL_USE_TLS)
            if self.config.MAIL_USE_TLS or self.config.MAIL_USE_SSL:
                await smtp.starttls()
            if self.config.MAIL_USERNAME and self.config.MAIL_PASSWORD:
                await smtp.login(self.config.MAIL_USERNAME, self.config.MAIL_PASSWORD)

            mime_message = await self._create_mime_message(message, template_name)
            await smtp.send_message(mime_message)
        except Exception as error:
            # Consider adding logging here
            raise EmailSendError(f"Failed to send email: {error}")
        finally:
            if smtp.is_connected:
                await smtp.quit()


    async def _create_mime_message(
        self, message: EmailMessage, template_name: Optional[str] = None
    ) -> MIMEMultipart:
        """Creates a MIME message from an EmailMessage object."""
        mime_message = MIMEMultipart("mixed" if message.attachments else "alternative")
        mime_message["Subject"] = message.subject
        mime_message["From"] = (
            message.sender if message.sender else self.config.MAIL_DEFAULT_SENDER
        )
        mime_message["To"] = ", ".join(message.recipients)

        # If a template is provided, render the email content using the template
        if template_name and self.template_manager:
            rendered_content = self.template_manager.render_template(
                template_name, message.template_body
            )
            mime_message.attach(MIMEText(rendered_content, "html"))
        else:
            if message.body:
                mime_message.attach(MIMEText(message.body, "plain"))
            if message.html_body:
                mime_message.attach(MIMEText(message.html_body, "html"))

        # Handling attachments
        for attachment_path in message.attachments:
            attachment = message.create_attachment(attachment_path)
            mime_message.attach(attachment)

        return mime_message
