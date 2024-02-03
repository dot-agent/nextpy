from typing import Any, Dict, Union
from nextpy.ai.agent.base_agent import BaseAgent
import logging
from pathlib import Path
from nextpy.ai import engine
from typing import Callable, Tuple
import inspect
import asyncio


def _call_functions(functions):
    for function, arguments, keyword_args in functions:
        if inspect.iscoroutinefunction(function):
            try:
                other_loop = asyncio.get_event_loop()
                import nest_asyncio

                nest_asyncio.apply(other_loop)
            except RuntimeError:
                pass
            loop = asyncio.new_event_loop()
            loop.run_until_complete(function(*arguments, **keyword_args))
        else:
            function(*arguments, **keyword_args)


async def _a_call_functions(functions):
    for function, arguments, keyword_args in functions:
        if inspect.iscoroutinefunction(function):
            await function(*arguments, **keyword_args)
        else:
            function(*arguments, **keyword_args)


class AssistantAgent(BaseAgent):
    """
    AssistantAgent class represents an assistant agent that interacts with users in a conversational manner.

    :param name: The name of the assistant agent.
    :type name: str
    :param llm: The language model used by the assistant agent.
    :type llm: LanguageModel
    :param memory: The memory used by the assistant agent.
    :type memory: Memory
    :param async_mode: Whether the assistant agent should run in asynchronous mode or not. Default is True.
    :type async_mode: bool, optional
    :param system_message: The system message included in the prompt. Default is None.
    :type system_message: str, optional
    :param functions_before_call: List of functions to be called before the main function call. Default is None.
    :type functions_before_call: List[Callable], optional
    :param functions_after_call: List of functions to be called after the main function call. Default is None.
    :type functions_after_call: List[Callable], optional
    """

    DEFAULT_PROMPT = '''
    {{#system~}} {{name}}, you are working in the following team :{{agents}}
    {{~/system}}
    
    {{#user~}}
    Read the following CONVERSATION :
    {{messages}}
    Respond. Do not thank any team member or show appreciation."
    {{~/user}}
    
    {{#assistant~}}
    {{gen 'answer' temperature=0 max_tokens=500}}
    {{~/assistant}}
    '''

    def __init__(self,
                 name,
                 llm=None,
                 memory=None,
                 async_mode: bool = False,
                 system_message: str | None = None,
                 custom_engine=None,
                 functions_before_call: Tuple[Callable,
                                              Tuple[Any], Tuple[Any]] | None = None,
                 functions_after_call: Tuple[Callable,
                                             Tuple[Any], Tuple[Any]] | None = None,
                 **kwargs):
        """
        Initializes an instance of the AssistantAgent class.

        :param name: The name of the assistant agent.
        :type name: str
        :param llm: The language model used by the assistant agent.
        :type llm: LanguageModel
        :param memory: The memory used by the assistant agent.
        :type memory: Memory
        :param async_mode: Whether the assistant agent should run in asynchronous mode or not. Default is True.
        :type async_mode: bool, optional
        :param system_message: The system message to be displayed to the user. Default is None.
        :type system_message: str, optional
        :param engine: The engine used by the assistant agent. Either llm or engine must be provided.
        :type engine: Engine, optional
        :param functions_before_call: List of functions, args and kwargs, to be called before the main function call. Default is None.
        :type functions_before_call: List[Callable], optional
        :param functions_after_call: List of functions, args and kwargs to be called after the main function call. Default is None.
        :type functions_after_call: List[Callable], optional
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(llm=llm, **kwargs)
        self.prompt = self.DEFAULT_PROMPT
        self.system_message = system_message
        # This is used by multiagent manager to determine whether to use receive or a_receive
        self.async_mode = async_mode

        if system_message is not None:
            try:
                system_message = Path(system_message).read_text()
            except Exception:
                pass
            self.prompt = self.prompt[:self.DEFAULT_PROMPT.find(
                '{{~/system}}')] + system_message + self.prompt[self.DEFAULT_PROMPT.find('{{~/system}}'):]

        # Either llm or engine must be provided
        assert llm is not None or engine is not None, "Either llm or engine must be provided."

        self.engine = custom_engine if custom_engine is not None else engine(
            template=self.prompt, llm=llm, memory=memory, async_mode=async_mode, **kwargs)
        self.output_key = 'answer'
        self.name = name
        self.functions_before_call = functions_before_call
        self.functions_after_call = functions_after_call

    @staticmethod
    def function_call_decorator(func):
        """
        Decorator function that wraps the main function call with additional functions to be called before and after.

        :param func: The main function to be called.
        :type func: Callable
        :return: The wrapped function.
        :rtype: Callable
        """
        if inspect.iscoroutinefunction(func):
            async def a_inner(self, *args, **kwargs):
                if self.functions_before_call is not None:
                    await _a_call_functions(self.functions_before_call)

                result = await func(self, *args, **kwargs)

                if self.functions_after_call is not None:
                    await _a_call_functions(self.functions_after_call)

                return result
            return a_inner
        else:
            def inner(self, *args, **kwargs):
                if self.functions_before_call is not None:
                    _call_functions(self.functions_before_call)

                result = func(self, *args, **kwargs)

                if self.functions_after_call is not None:
                    _call_functions(self.functions_after_call)

                return result
            return inner

    @function_call_decorator
    def receive(self, agents, messages, termination_message):
        """
        Receives messages from other agents and generates a response.

        :param agents: The list of agents involved in the conversation.
        :type agents: List[str]
        :param messages: The list of messages in the conversation.
        :type messages: List[str]
        :param termination_message: The termination message for the conversation.
        :type termination_message: str
        :return: The generated response.
        :rtype: str
        """
        output = self.run(agents=agents, messages=messages, name=self.name)
        return output

    @function_call_decorator
    async def a_receive(self, agents, messages, termination_message):
        """
        Asynchronously receives messages from other agents and generates a response.

        :param agents: The list of agents involved in the conversation.
        :type agents: List[str]
        :param messages: The list of messages in the conversation.
        :type messages: List[str]
        :param termination_message: The termination message for the conversation.
        :type termination_message: str
        :return: The generated response.
        :rtype: str
        """
        output = await self.arun(agents=agents, messages=messages, name=self.name)
        return output
