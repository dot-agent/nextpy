from nextpy.ai.agent.assistant_agent import AssistantAgent
from typing import Any, Tuple, Callable


class UserProxyAgent(AssistantAgent):

    def __init__(self,
                 async_mode: bool = False,
                 functions_before_call: Tuple[Callable,
                                              Tuple[Any], Tuple[Any]] | None = None,
                 functions_after_call: Tuple[Callable,
                                             Tuple[Any], Tuple[Any]] | None = None,
                 description: str = "User Proxy Agent capable of receiving user input.",
                 **kwargs):
        self.name = 'User'
        self.description = description
        self.async_mode = async_mode
        self.functions_before_call = functions_before_call
        self.functions_after_call = functions_after_call

    @AssistantAgent.function_call_decorator
    def receive(self, *args, **kwargs):
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
        return self._receive_user_input()

    @AssistantAgent.function_call_decorator
    async def a_receive(self, *args, **kwargs):
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
        return await self.a_receive_user_input()

    def _receive_user_input(self):
        """
        Receives user input and returns it as the response.

        :return: The user input.
        :rtype: str
        """
        return input('Provide feedback to chat_manager:')

    async def a_receive_user_input(self):
        """
        Asynchronously receives user input and returns it as the response.

        :return: The user input.
        :rtype: str
        """
        return input('Provide feedback to chat_manager:')
