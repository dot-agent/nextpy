"""Notion tool spec."""

#from llama_index.tools.tool_spec.base import BaseToolSpec
from openams.tools.toolkits.notion_toolkit.notion.utils import NotionPageReader
from openams.tools.basetool import BaseTool
from typing import Optional, List, Type, Dict, Any
import requests
from pydantic import BaseModel, Field

SEARCH_URL = "https://api.notion.com/v1/search"


class NotionLoadDataSchema(BaseModel):
    """Notion load data schema."""

    page_ids: Optional[List[str]] = None
    database_id: Optional[str] = None


class NotionSearchDataSchema(BaseModel):
    """Notion search data schema."""

    query: str
    direction: Optional[str] = None
    timestamp: Optional[str] = None
    value: Optional[str] = None
    property: Optional[str] = None
    page_size: int = 100

class NotionBase(BaseTool):

    def __init__(self, integration_token: Optional[str] = None) -> None:
        """Initialize with parameters."""
        self.reader = NotionPageReader(integration_token=integration_token)


class LoadDataArgsSchema(BaseModel):
    page_ids: Optional[List[str]] = Field(
        ...,
        description="******Provide Description About PageId*******"
    )
    database_id: Optional[str] = Field(
        ...,
        description="******Description about this Parameter********"
    )

class SearchDataArgsSchema(BaseModel):
    query: str = Field(
        ...,
        description="Info about parameter"
    )
    direction: Optional[str] = Field(
        ...,
        description="Info about parameter"
    )
    timestamp: Optional[str] = Field(
        ...,
        description="Info about parameter"
    )
    value: Optional[str] = Field(
        ...,
        description="Info about parameter"
    )
    property: Optional[str] = Field(
        ...,
        description="Info about parameter"
    )
    page_size: int = Field(
        ...,
        description="Info about parameter"
    )

class LoadData(NotionBase):
    name : str = "Load Data"
    description : str = "Loads content from a set of page ids or a database id."
    args_schema : Type[LoadDataArgsSchema] = LoadDataArgsSchema

    def load_data(
        self, page_ids: Optional[List[str]] = None, database_id: Optional[str] = None
    ) -> str:
        """Loads content from a set of page ids or a database id.

        Don't use this endpoint if you don't know the page ids or database id.

        """
        page_ids = page_ids or []
        docs = self.reader.load_data(page_ids=page_ids, database_id=database_id)
        return "\n".join([doc.get_content() for doc in docs])
    
    def run(
        self, page_ids: Optional[List[str]] = None, database_id: Optional[str] = None
    ) -> str:
        try:
            return self.load_data(self, page_ids=page_ids, database_id=database_id)
        except Exception as e:
            return e

    
class SearchData(NotionBase):
    name: str = "Search Data"
    description: str = "Search a list of relevant pages.Contains metadata for each page (but not the page content)"
    args_schema: Type[SearchDataArgsSchema] = SearchDataArgsSchema
    def search_data(
        self,
        query: str,
        direction: Optional[str] = None,
        timestamp: Optional[str] = None,
        value: Optional[str] = None,
        property: Optional[str] = None,
        page_size: int = 100,
    ) -> str:
        """Search a list of relevant pages.

        Contains metadata for each page (but not the page content).

        """
        payload: Dict[str, Any] = {
            "query": query,
            "page_size": page_size,
        }
        if direction is not None or timestamp is not None:
            payload["sort"] = {}
            if direction is not None:
                payload["sort"]["direction"] = direction
            if timestamp is not None:
                payload["sort"]["timestamp"] = timestamp

        if value is not None or property is not None:
            payload["filter"] = {}
            if value is not None:
                payload["filter"]["value"] = value
            if property is not None:
                payload["filter"]["property"] = property

        response = requests.post(SEARCH_URL, json=payload, headers=self.reader.headers)
        response_json = response.json()
        response_results = response_json["results"]
        return response_results
    
    def run(
        self,
        query: str,
        direction: Optional[str] = None,
        timestamp: Optional[str] = None,
        value: Optional[str] = None,
        property: Optional[str] = None,
        page_size: int = 100,
    ) -> str:
        try:
            return self.search_data(
                query=query,
                direction=direction,
                timestamp=timestamp,
                value=value,
                property=property,
                page_size=page_size
            )
        except Exception as e:
            return e