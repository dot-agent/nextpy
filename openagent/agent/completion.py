from enum import Enum
from typing import List, Dict, Any, Union, Optional
import os
from openagent import compiler
from openagent.tools.basetool import BaseTool
from openagent.agent.base_agent import BaseAgent
import logging
import yaml
import argparse

class AgentState(Enum):
    """Enum to represent different states of the Agent"""

    IDLE = 0
    BUSY = 1
    USED_AS_TOOL = 2
    ERROR = 3

class TextCompletionAgent(BaseAgent):
    def __init__(self,
                knowledgebase: Optional[Any] = None,
                tools: Optional[Any] = None,
                llm: Optional[Any] = None,
                prompt_template: str = "{{input}} {{gen 'output'}}",
                input_variables: Dict = {},
                agent_id: str = "default",
                memory: Any = None,
                caching: bool = False,
                output_key: str = None,
                return_complete: bool = False
                ):
        
        self.agent_id = agent_id
        self.knowledgebase = knowledgebase
        self.tools = tools
        self.prompt_template = prompt_template
        self.input_variables = input_variables
        self.memory = memory
        self.state = AgentState.IDLE
        self.caching = caching
        self.return_complete = return_complete
        self.llm = llm if llm is not None else self.llm_instance()

        self.parser = argparse.ArgumentParser(description="CLI for interacting with the Agent instance.")

        self.output_key = output_key
        self.compiler = compiler(llm = self.llm, template = self.prompt_template, caching=caching)

        if self.return_complete and self.output_key is not None:
            logging.warning("return_complete mode is enabled. Output key will be ignored.")

        if self.knowledgebase is not None and not self.input_variables.get('knowledge_variable'):
            raise ValueError ("knowledge_variable should be present in input_variables while using knowledge")
        

    @property
    def agent_type(self):
        return "completion"

    @property
    def get_knowledge_variable(self):
        """Get knowledge variable name from input variables"""
        return self.input_variables.get('knowledge_variable')
    
    @property
    def default_llm_model(self):
        return "text-davinci-003"
        
    def add_tool(self, tool: BaseTool) -> None:
        """Add a tool to the agent's tool list."""
        self.tools.append(tool)

    def remove_tool(self, tool: BaseTool) -> None:
        """Remove a tool from the agent's tool list."""
        if tool in self.tools:
            self.tools.remove(tool)

    def llm_instance(self) -> compiler.llms.OpenAI:
        """Create an instance of the language model."""
        return compiler.llms.OpenAI(model=self.default_llm_model)
    
    def get_output_key(self, prompt):
        vars = prompt.variables()
        vars = list(vars.keys())
        return vars[-1]

    def get_knowledge(self, query) -> List[str]:
        docs = self.knowledgebase.retrieve_data(query)
        final_doc = ""
        for doc in docs:
            final_doc += doc
        return final_doc

    
