import mimetypes
import os
from email import encoders
from email.mime.base import MIMEBase
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, EmailStr, validator


class MessageType(str, Enum):
    PLAIN = "plain"
    HTML = "html"

class MultipartSubtypeEnum(str, Enum):
    MIXED = "mixed"
    DIGEST = "digest"
    ALTERNATIVE = "alternative"
    RELATED = "related"
    REPORT = "report"
    SIGNED = "signed"
    ENCRYPTED = "encrypted"
    FORM_DATA = "form-data"
    MIXED_REPLACE = "x-mixed-replace"
    BYTERANGE = "byterange"

class EmailMessage(BaseModel):
    recipients: List[EmailStr]
    subject: str
    body: Optional[str] = None
    html_body: Optional[str] = None
    sender: Optional[EmailStr] = None
    cc: List[EmailStr] = []
    bcc: List[EmailStr] = []
    attachments: List[str] = []  # List of file paths for attachments
    template_body: Optional[Union[dict, list, str]] = None  # Template context
    subtype: MessageType = MessageType.PLAIN
    multipart_subtype: MultipartSubtypeEnum = MultipartSubtypeEnum.MIXED
    headers: Optional[Dict[str, str]] = None

    @validator('attachments', each_item=True)
    def validate_attachment(cls, v):
        if isinstance(v, str) and os.path.isfile(v) and os.access(v, os.R_OK):
            return v
        raise ValueError("Attachment must be a readable file path")

    def create_attachment(self, filepath: str) -> MIMEBase:
        """Creates a MIMEBase object for the given attachment file."""
        ctype, encoding = mimetypes.guess_type(filepath)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(filepath, 'rb') as fp:
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath))
        return attachment

    class Config:
        arbitrary_types_allowed = True
