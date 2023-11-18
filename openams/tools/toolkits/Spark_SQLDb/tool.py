"""Tools for interacting with a SQL database."""
from typing import Any, Dict, Optional

from pydantic import BaseModel, Extra, Field, root_validator
from openams.helpers.spark_sql_database import SparkSQL
from openams.tools.basetool import BaseTool
from openams.tools.toolkits.Spark_SQLDb.prompt import QUERY_CHECKER

class BaseSparkSQLTool(BaseModel):
    """Base tool for interacting with Spark SQL."""

    db: SparkSQL = Field(exclude=True)

    # Override BaseTool.Config to appease mypy
    # See https://github.com/pydantic/pydantic/issues/4173
    class Config(BaseTool.Config):
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True
        extra = Extra.forbid


class QuerySparkSQLTool(BaseSparkSQLTool, BaseTool):
    """Tool for querying a Spark SQL."""

    name = "query_sql_db"
    description = """
    Input to this tool is a detailed and correct SQL query, output is a result from the Spark SQL.
    If the query is not correct, an error message will be returned.
    If an error is returned, rewrite the query, check the query, and try again.
    """

    def run(
        self,
        query: str,
    ) -> str:
        """Execute the query, return the results or an error message."""
        return self.db.run_no_throw(query)

    async def arun(
        self,
        query: str,
    ) -> str:
        raise NotImplementedError("QuerySqlDbTool does not support async")


class InfoSparkSQLTool(BaseSparkSQLTool, BaseTool):
    """Tool for getting metadata about a Spark SQL."""

    name = "schema_sql_db"
    description = """
    Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables.
    Be sure that the tables actually exist by calling list_tables_sql_db first!

    Example Input: "table1, table2, table3"
    """

    def run(
        self,
        table_names: str,
    ) -> str:
        """Get the schema for tables in a comma-separated list."""
        return self.db.get_table_info_no_throw(table_names.split(", "))

    async def arun(
        self,
        table_name: str,
    ) -> str:
        raise NotImplementedError("SchemaSqlDbTool does not support async")


class ListSparkSQLTool(BaseSparkSQLTool, BaseTool):
    """Tool for getting tables names."""

    name = "list_tables_sql_db"
    description = "Input is an empty string, output is a comma separated list of tables in the Spark SQL."

    def run(
        self,
        tool_input: str = "",
    ) -> str:
        """Get the schema for a specific table."""
        return ", ".join(self.db.get_usable_table_names())

    async def arun(
        self,
        tool_input: str = "",
    ) -> str:
        raise NotImplementedError("ListTablesSqlDbTool does not support async")

#QueryCheckerTool uses LLMChain which needs to be solved
'''
class QueryCheckerTool(BaseSparkSQLTool, BaseTool):
    """Use an LLM to check if a query is correct.
    Adapted from https://www.patterns.app/blog/2023/01/18/crunchbot-sql-analyst-gpt/"""

    template: str = QUERY_CHECKER
    llm: BaseLanguageModel
    llm_chain: LLMChain = Field(init=False)
    name = "query_checker_sql_db"
    description = """
    Use this tool to double check if your query is correct before executing it.
    Always use this tool before executing a query with query_sql_db!
    """

    @root_validator(pre=True)
    def initialize_llm_chain(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if "llm_chain" not in values:
            values["llm_chain"] = LLMChain(
                llm=values.get("llm"),
                prompt=PromptTemplate(
                    template=QUERY_CHECKER, input_variables=["query"]
                ),
            )

        if values["llm_chain"].prompt.input_variables != ["query"]:
            raise ValueError(
                "LLM chain for QueryCheckerTool need to use ['query'] as input_variables "
                "for the embedded prompt"
            )

        return values

    def _run(
        self,
        query: str,
    ) -> str:
        """Use the LLM to check the query."""
        return self.llm_chain.predict(query=query)

    async def _arun(
        self,
        query: str,
    ) -> str:
        return await self.llm_chain.apredict(query=query)
'''