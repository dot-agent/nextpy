from enum import Enum
from typing import List, Dict, Any, Union, Optional
import os
from openagent import compiler
from openagent.tools.basetool import BaseTool
import logging
import yaml
import yaml
import importlib
import argparse

def import_class(class_path):
    module_name, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)

class AgentState(Enum):
    """Enum to represent different states of the Agent"""

    IDLE = 0
    BUSY = 1
    USED_AS_TOOL = 2
    ERROR = 3


class BaseAgent:
    def __init__(self,
                knowledgebase: Optional[Any] = None,
                tools: Optional[Any] = None,
                llm: Optional[Any] = None,
                prompt_template: str = None,
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
        self.llm = llm
        self.prompt_template = prompt_template
        self.input_variables = input_variables
        self.memory = memory
        self.state = AgentState.IDLE
        self.caching = caching
        self.return_complete = return_complete
        self.llm = llm if llm is not None else self.llm_instance()

        self.output_key = output_key
        self.compiler = compiler(llm = self.llm, template = self.prompt_template, caching=caching)

        if self.return_complete and self.output_key is not None:
            logging.warning("return_complete mode is enabled. Output key will be ignored.")

        if self.knowledgebase is not None and not self.input_variables.get('knowledge_variable'):
            raise ValueError ("knowledge_variable should be present in input_variables while using knowledge")


    @property
    def agent_type(self):
        pass

    @property
    def get_knowledge_variable(self):
        """Get knowledge variable name from input variables"""
        pass
    
    @property
    def default_llm_model(self):
        pass
        
    def add_tool(self, tool: BaseTool) -> None:
        """Add a tool to the agent's tool list."""
        self.tools.append(tool)

    def remove_tool(self, tool: BaseTool) -> None:
        """Remove a tool from the agent's tool list."""
        if tool in self.tools:
            self.tools.remove(tool)

    def llm_instance(self) -> compiler.llms.OpenAI:
        """Create an instance of the language model."""
        pass
    
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

    def run(self, **kwargs) -> Union[str, Dict[str, Any]]:
        """Run the agent to generate a response to the user query."""
    
        _knowledge_variable = self.get_knowledge_variable

        if _knowledge_variable:
            if kwargs.get(_knowledge_variable):
                query = kwargs.get(_knowledge_variable)
                retrieved_knowledge = self.get_knowledge(query)
                output = self.compiler(RETRIEVED_KNOWLEDGE = retrieved_knowledge, **kwargs, silent = True)
            else:
                raise ValueError("knowledge_variable not found in input kwargs")
        else:
            output = self.compiler(**kwargs, silent = True)

        if self.return_complete:
            return output
        
        _output_key = self.output_key if self.output_key is not None else self.get_output_key(output)

        if output.variables().get(_output_key):
            return output[_output_key]
        else:
            logging.warning("Output key not found in output, so full output returned")
            return output
        

    def cli(self):
        """Start a CLI for interacting with the agent."""
        print("Welcome to the agent CLI!")

        _vars = []
        for _, v in self.input_variables.items():
            if isinstance(v, str):
                _vars.append(v)
            if isinstance(v, List):
                _vars.extend(v)
        
        parser = argparse.ArgumentParser(description="CLI for interacting with the Agent instance.")

        for var in _vars:
            parser.add_argument(f"--{var}", help=f"Pass {var} as an input variable")

        args = parser.parse_args()
        
        print(self.run(**vars(args)))


    def cli_inputs(self):
        """Start a CLI for interacting with the agent."""
        print("Welcome to the agent CLI!")

        _vars = []
        kwargs = {}
        for _, v in self.input_variables.items():
            if isinstance(v, str):
                _vars.append(v)
            if isinstance(v, List):
                _vars.extend(v)

        for var in _vars:
            kwargs[var] = input(f"{var}: ".capitalize())
        
        print(self.run(**kwargs))


        # if self.state != AgentState.IDLE:
        #     return {"error": "Agent is not in idle state."}

        # self.state = AgentState.BUSY
        # try:
        #     if self.user_query:
        #         output = self.engine()()  # Create and run the engine in one line
        #         return output
        #     else:
        #         return f"I'm {self.agent_id}. What can I help you with?"
        # except Exception as e:
        #     self.state = AgentState.ERROR
        #     print(f"An error occurred: {e}")
        #     raise e
        # finally:
        #     self.state = AgentState.IDLE


    # def export_agent_config(self, config_path):
    #     config = {
    #         'llm': {
    #             'type': f"{self.llm.__class__.__name__}",
    #             'model': self.llm.model_name
    #         },
    #         'knowledgebase': None if self.knowledgebase is None else {
    #             'data_references': self.knowledgebase.references,
    #             'data_transformer': {
    #                 'type': self.knowledgebase.data_transformer.__class__.__module__ + '.' +
    #                         self.knowledgebase.data_transformer.__class__.__name__,
    #                 'chunk_overlap': self.knowledgebase.data_transformer._chunk_overlap,
    #                 'chunk_size': self.knowledgebase.data_transformer._chunk_size
    #             },
    #             'vector_store': {
    #                 'type': self.knowledgebase.vector_store.__class__.__module__ + '.' +
    #                         self.knowledgebase.vector_store.__class__.__name__,
    #                 'embedding_function': self.knowledgebase.vector_store._embedding_function
    #             }
    #         },
    #         'memory' : None if self.memory is None else {
    #             'type' : self.memory.__class__.__module__ + '.' +
    #                     self.memory.__class__.__name__,
    #         },
    #         'agent': {
    #             'type': f"{self.__class__.__name__}",
    #             'prompt_template': self.prompt_template,
    #             'input_variables': self.input_variables,
    #             'output_key': self.output_key
    #         }
    #     }

    #     with open(config_path, 'w') as f:
    #         yaml.safe_dump(config, f)


    # def from_config(config_path):
    #     with open(config_path, 'r') as f:
    #         config = yaml.safe_load(f)

    #     llm_class = import_class(config['llm']['type'])
    #     llm = llm_class(model_name=config['llm']['model'])

    #     data_transformer_class = import_class(config['knowledgebase']['data_transformer']['type'])
    #     data_transformer = data_transformer_class(
    #         chunk_overlap=config['knowledgebase']['data_transformer']['chunk_overlap'],
    #         chunk_size=config['knowledgebase']['data_transformer']['chunk_size']
    #     )

    #     vector_store_class = import_class(config['knowledgebase']['vector_store']['type'])
    #     vector_store = vector_store_class(embedding_function=config['knowledgebase']['vector_store']['embedding_function'])

    #     agent_class = import_class(config['agent']['type'])
    #     agent = agent_class(
    #         llm=llm,
    #         data_source=config['knowledgebase']['data_source'],
    #         data_loader=config['knowledgebase']['data_loader'],
    #         data_transformer=data_transformer,
    #         vector_store=vector_store,
    #         prompt_template=config['agent']['prompt_template'],
    #         input_variables=config['agent']['input_variables'],
    #         output_key=config['agent']['output_key']
    #     )

    #     return agent
    

    def print_config(self):
        print("Language Model:")
        print(f" - Type: {self.llm.__class__.__name__}")
        print(f" - Model: {self.llm.model_name}")
        
        if self.knowledgebase:
            print("\nKnowledge Base:")
            print(f" - Data References: {self.knowledgebase.references}")
            print(f" - Data Transformer: {self.knowledgebase.data_transformer}")
            print(f" - Vector Store: {self.knowledgebase.vector_store}")

        if self.memory:
            print("\nMemory:")
            print(f" - Type: {self.memory}")
        
        print("\nAgent:")    
        print(f" - Type: {self.__class__.__name__}")
        print(f" - Prompt Template: {self.prompt_template}")
        print(f" - Input Variables: {self.input_variables}")
        print(f" - Output Key: {self.output_key}")


