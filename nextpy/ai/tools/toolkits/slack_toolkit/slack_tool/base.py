import logging
from datetime import datetime
from ssl import SSLContext
from typing import List, Optional, Type

import pydantic
from pydantic import BaseModel, Field

from nextpy.ai.schema import Document
from nextpy.ai.tools.basetool import BaseTool
from nextpy.ai.tools.toolkits.slack_toolkit.slack_tool.utils import SlackReader

logger = logging.getLogger(__name__)


class SlackBase(BaseTool):
    """Slack toolkit."""

    reader: Optional[SlackReader] = Field(None)
    slack_token: Optional[str] = Field(None)
    ssl: Optional[SSLContext] = Field(None)
    earliest_date: Optional[datetime] = Field(None)
    latest_date: Optional[datetime] = Field(None)

    class Config:
        arbitrary_types_allowed = True

    @pydantic.validator("reader", pre=True, always=True)
    def set_reader(cls, v, values):
        return SlackReader(
            slack_token=values.get("slack_token"),
            ssl=values.get("ssl"),
            earliest_date=values.get("earliest_date"),
            latest_date=values.get("latest_date"),
        )


class LoadDataArgsSchema(BaseModel):
    channel_ids: List[str] = Field(
        ...,
        description="List of IDs for the Slack channels from which to load data",
    )
    reverse_chronological: bool = Field(
        ...,
        description="Signifies whether the loaded data should be ordered in reverse chronological order. By default, it's set to True",
    )


class LoadData(SlackBase):
    name: str = "load_data"
    description: str = "Load data from the input directory."
    args_schema: Type[LoadDataArgsSchema] = LoadDataArgsSchema

    def load_data(
        self,
        channel_ids: List[str],
        reverse_chronological: bool = True,
    ) -> List[Document]:
        """Load data from the input directory."""
        return self.reader.load_data(
            channel_ids=channel_ids,
            reverse_chronological=reverse_chronological,
        )

    def run(
        self,
        channel_ids: List[str],
        reverse_chronological: bool = True,
    ) -> str:
        """Run the tool."""
        try:
            return self.load_data(
                self,
                channel_ids=channel_ids,
                reverse_chronological=reverse_chronological,
            )
        except Exception as e:
            raise Exception(f"An error occurred: {e}")


class FetchChannel(SlackBase):
    name: str = "fetch_channel"
    description: str = "Fetch a list of relevant channels"

    def fetch_channels(
        self,
    ) -> List[str]:
        """Fetch a list of relevant channels."""
        slack_client = self.reader.client
        try:
            msg_result = slack_client.conversations_list()
            logger.info(msg_result)
        except Exception as e:
            logger.error(e)
            raise e

        return msg_result["channels"]

    def _run(
        self,
    ) -> str:
        """Run the tool."""
        return self.fetch_channels()


class SendMessageArgsSchema(BaseModel):
    channel_id: str = Field(
        ...,
        description="ID of the channel to send message to",
    )
    message: str = Field(
        ...,
        description="Content of the message",
    )


class SendMessage(SlackBase):
    name: str = "send_message"
    description: str = "Send a message to a channel given the channel ID."
    args_schema: Type[SendMessageArgsSchema] = SendMessageArgsSchema

    def send_message(
        self,
        channel_id: str,
        message: str,
    ) -> None:
        """Send a message to a channel given the channel ID."""
        slack_client = self.reader.client
        try:
            msg_result = slack_client.chat_postMessage(
                channel=channel_id,
                text=message,
            )
            logger.info(msg_result)
        except Exception as e:
            logger.error(e)
            raise e

    def _run(
        self,
        channel_id: str,
        message: str,
    ) -> str:
        """Run the tool."""
        try:
            self.send_message(channel_id=channel_id, message=message)
            return "Message Sent"
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
