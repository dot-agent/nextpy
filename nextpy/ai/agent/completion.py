from typing import Any, Dict, List, Optional

from nextpy.ai.agent.base_agent import BaseAgent
from nextpy.ai.tools.basetool import BaseTool


class TextCompletionAgent(BaseAgent):
    """Text completion agent class based on the BaseAgent class."""

    def __init__(
        self,
        rag: Optional[Dict] = None,
        tools: Optional[List[BaseTool]] = None,
        llm: str = None,
        prompt_template: str = None,
        input_variables: Dict[str, Any] = {},
        agent_id: str = "default",
        memory: Dict = None,
        caching: bool = False,
        output_key: str = None,
        return_complete: bool = False,
    ):
        super().__init__(
            rag,
            tools,
            llm,
            prompt_template,
            input_variables,
            agent_id,
            memory,
            caching,
            output_key,
            return_complete,
        )

    @property
    def agent_type(self):
        return "completion"

    @property
    def default_llm_model(self):
        return "text-davinci-003"
