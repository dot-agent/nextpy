from openams.schema import Document
from openams.tools.toolkits.slack_toolkit.slack.utils import SlackReader
from openams.tools.basetool import BaseTool
from typing import Optional, List, Type
from ssl import SSLContext
from pydantic import BaseModel, Field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SlackBase(BaseTool):

    def __init__(
            self,
            slack_token: Optional[str] = None,
            ssl: Optional[SSLContext] = None,
            earliest_date: Optional[datetime] = None,
            latest_date: Optional[datetime] = None,
        ) -> None:
            """Initialize with parameters."""
            self.reader = SlackReader(
                slack_token=slack_token,
                ssl=ssl,
                earliest_date=earliest_date,
                latest_date=latest_date,
            )

class LoadDataArgsSchema(BaseModel):
    channel_ids: List[str] = Field(
        ...,
        description=" Information about the parameter. ",
    )
    reverse_chronological: bool = Field(
        ...,
        description=" Information about the parameter.",
    )

class LoadData(SlackBase):
    name: str = "load_data"
    description: str = "Load data from the input directory."
    args_schema : Type[LoadDataArgsSchema] = LoadDataArgsSchema

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
    def _run(
            self,
            channel_ids: List[str],
            reverse_chronological: bool = True,
        )-> str:
         """Run the tool."""
         try:
            return self.load_data(self, channel_ids=channel_ids, reverse_chronological=reverse_chronological)
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
        )-> str:
         """Run the tool."""
         return self.fetch_channels()

class SendMessageArgsSchema(BaseModel):
    channel_id: str = Field(
        ...,
        description=" Information about the parameter. ",
    )
    message: str = Field(
        ...,
        description=" Information about the parameter. ",
    )
class SendMessage(SlackBase):
    name: str = "send_message"
    description: str = "Send a message to a channel given the channel ID."
    args_schema : Type[SendMessageArgsSchema] = SendMessageArgsSchema
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
        )-> str:
         """Run the tool."""
         try:
            self.send_message(channel_id=channel_id, message=message)
            return "Message Sent"
         except Exception as e:
            raise Exception(f"An error occurred: {e}")
        