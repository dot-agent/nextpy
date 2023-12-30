# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.


import logging
from pathlib import Path
from typing import Any, Dict, Union

import pkg_resources as pg
from dotagent import compiler
from dotagent.agent.base_agent import BaseAgent
from dotagent.llms._openai import OpenAI
from dotagent.memory import SimpleMemory

path = pg.resource_filename(__name__, 'prompt.hbs')
salesagent_prompt_template = Path(path).read_text()

sales_coversation_memory = SimpleMemory()

class SalesAgent(BaseAgent):

    def __init__(self,
                 use_tools: bool = False,
                 prompt_template :str = salesagent_prompt_template,
                salesperson_name: str = "Ted Lasso",
                salesperson_role: str = "Business Development Representative",
                company_name: str = "Sleep Haven",
                company_business: str = "Sleep Haven is a premium mattress company that provides customers with the most comfortable and supportive sleeping experience possible. We offer a range of high-quality mattresses, pillows, and bedding accessories that are designed to meet the unique needs of our customers.",
                company_values: str = "Our mission at Sleep Haven is to help people achieve a better night's sleep by providing them with the best possible sleep solutions. We believe that quality sleep is essential to overall health and well-being, and we are committed to helping our customers achieve optimal sleep by offering exceptional products and customer service.",
                conversation_purpose: str = "find out whether they are looking to achieve better sleep via buying a premier mattress.",
                conversation_type: str = "call",
                memory = sales_coversation_memory,
                 **kwargs):
        super().__init__(**kwargs)

        self.prompt_template = prompt_template
        self.use_tools = use_tools
        self.salesperson_name = salesperson_name
        self.salesperson_role = salesperson_role
        self.company_name = company_name
        self.company_business = company_business
        self.company_values = company_values
        self.conversation_purpose = conversation_purpose
        self.conversation_type = conversation_type
        self.memory = memory

        self.llm = OpenAI('gpt-3.5-turbo')

        self.compiler = compiler(
            llm = self.llm,
            template = self.prompt_template,
            salesperson_name = salesperson_name,
            salesperson_role = salesperson_role,
            company_name = company_name,
            company_business = company_business,
            company_values = company_values,
            conversation_purpose = conversation_purpose,
            conversation_type = conversation_type,
            caching=kwargs.get('caching'),
            memory = self.memory
            )

    def agent_type(self):
        return "chat"
    
    def run(self, **kwargs) -> Union[str, Dict[str, Any]]:
        """Run the agent to generate a response to the user query."""
        _data_variable = self.get_data_variable

        if _data_variable:
            if kwargs.get(_data_variable):
                query = kwargs.get(_data_variable)
                retrieved_knowledge = self.get_knowledge(query)
                output = self.compiler(RETRIEVED_KNOWLEDGE = retrieved_knowledge, **kwargs, silent = True)
            else:
                raise ValueError("data_variable not found in input kwargs")
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

        

