"""Slack toolkit."""

from openams.tools.toolkits.base import BaseToolkit
from openams.tools.basetool import BaseTool
from openams.tools.toolkits.slack_toolkit.slack_tool.utils import SlackReader
from openams.tools.toolkits.slack_toolkit.slack_tool.base import LoadData, FetchChannel, SendMessage
from typing import Optional, List
from ssl import SSLContext
import pydantic
import ssl
from pydantic import Field, validator
from datetime import datetime

class SlackToolkit(BaseToolkit):
    """Slack toolkit."""

    reader: Optional[SlackReader] = Field(None)
    slack_token: Optional[str] = Field(None)
    earliest_date: Optional[datetime] = Field(None)
    latest_date: Optional[datetime] = Field(None)

    class Config:
        arbitrary_types_allowed = True

    @validator('reader', pre=True, always=True)
    def set_reader(cls, v, values):
        # Create the SSLContext object here
        ssl_context = ssl.SSLContext()
        return SlackReader(
            slack_token=values.get('slack_token'),
            ssl=ssl_context,
            earliest_date=values.get('earliest_date'),
            latest_date=values.get('latest_date'),
        )

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            LoadData(
                    slack_token=self.slack_token,
                    ssl = self.ssl,
                    earliest_date = self.earliest_date,
                    latest_date = self.latest_date),
            FetchChannel(
                    slack_token=self.slack_token,
                    ssl = self.ssl,
                    earliest_date = self.earliest_date,
                    latest_date = self.latest_date),
            SendMessage(
                    slack_token=self.slack_token,
                    ssl = self.ssl,
                    earliest_date = self.earliest_date,
                    latest_date = self.latest_date),     
        ]


# class SlackToolkit(BaseToolkit):
#     """Slack toolkit."""

#     reader: Optional[SlackReader] = Field(None)

#     class Config:
#         arbitrary_types_allowed = True

#     def __init__(
#         self,
#         slack_token: Optional[str] = None,
#         ssl: Optional[SSLContext] = None,
#         earliest_date: Optional[datetime] = None,
#         latest_date: Optional[datetime] = None,
#     ) -> None:
#         """Initialize with parameters."""
#         self.reader: Optional[SlackReader] = None
#         self.reader = SlackReader(
#             slack_token=slack_token,
#             ssl=ssl,
#             earliest_date=earliest_date,
#             latest_date=latest_date,
#         )


# class SlackToolkit(BaseToolkit):
#     """Slack toolkit."""

#     reader: Optional[SlackReader] = Field(None)
#     slack_token: Optional[str] = Field(None)
#     ssl: Optional[SSLContext] = Field(None)
#     earliest_date: Optional[datetime] = Field(None)
#     latest_date: Optional[datetime] = Field(None)

#     class Config:
#         arbitrary_types_allowed = True

#     @pydantic.validator('reader', pre=True, always=True)
#     def set_reader(cls, v, values):
#         return SlackReader(
#             slack_token=values.get('slack_token'),
#             ssl=values.get('ssl'),
#             earliest_date=values.get('earliest_date'),
#             latest_date=values.get('latest_date'),
#          )