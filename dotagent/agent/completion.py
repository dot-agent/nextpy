from typing import List, Dict, Any, Optional

from dotagent.tools.basetool import BaseTool
from dotagent.agent.base_agent import BaseAgent


class TextCompletionAgent(BaseAgent):
    """
    Text completion agent class based on the BaseAgent class.
    """

    def __init__(
        self,
        knowledgebase: Optional[Dict] = None,
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
            knowledgebase,
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
