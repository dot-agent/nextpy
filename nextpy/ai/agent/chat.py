from typing import Dict, List, Optional

from nextpy.ai.agent.base_agent import BaseAgent
from nextpy.ai.tools.basetool import BaseTool


class ChatAgent(BaseAgent):
    """Chat agent class based on the BaseAgent class."""

    def __init__(
        self,
        rag: Optional[Dict] = None,
        tools: Optional[List[BaseTool]] = None,
        llm: str = None,
        prompt_template: str = None,
        input_variables: Dict = {},
        agent_id: str = "default",
        memory: Dict = None,
        caching: bool = False,
        output_key: str = None,
        return_complete: bool = False,
    ):
        super().__init__(
            rag=rag,
            tools=tools,
            llm=llm,
            prompt_template=prompt_template,
            input_variables=input_variables,
            agent_id=agent_id,
            memory=memory,
            caching=caching,
            output_key=output_key,
            return_complete=return_complete,
        )

        self.prompt_template = (
            prompt_template
            if prompt_template is not None
            else self.default_prompt_template
        )

    @property
    def agent_type(self):
        return "chat"

    @property
    def default_llm_model(self):
        return "gpt-3.5-turbo"

    @property
    def default_prompt_template(self):
        return """{{#user~}}
                    {{input}}
                    {{~/user}}                    
                    {{#assistant~}}
                    {{gen 'response'}}
                    {{~/assistant}}"""
