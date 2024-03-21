from typing import Tuple, List, Any
from nextpy.ai.agent.assistant_agent import AssistantAgent
from nextpy.ai import engine


class MultiAgentManager:
    """
    A class that manages multiple agents in a role-playing game.

    Attributes:
        DEFAULT_PROMPT (str): The default prompt for the game.
        SOLUTION_PROMPT (str): The prompt for generating the final solution.
        agents (Tuple[AssistantAgent]): A tuple of AssistantAgent objects representing the participating agents.
        messages (List[Any]): A list of messages exchanged between the agents and the user.
        termination_message (str): The termination message indicating the end of the game.
        error_message (str): The error message indicating an error in the game.
        mode (str): The mode of the game (e.g., 'BROADCAST', 'ROUND_ROBIN').
        rounds (int): The number of rounds to play.
        round_robin (bool): A flag indicating whether to use round-robin mode.
        llm: The language model used by the agents.
        memory: The memory used by the agents.
        async_mode (bool): A flag indicating whether to use asynchronous mode.
        debug_mode (bool): A flag indicating whether to enable debug mode.
    """
    DEFAULT_PROMPT = '''   
    {{#system~}} You are playing a role playing game with the following participants : \n{{agents}}{{~/system}}

    {{#user~}}
    Read the following conversation and choose who the next speaker will be:
    {{messages}}
    Simply respond with the NAME of the next speaker without any other characters such as numbers or punctuations.
    {{~/user}}

    {{#assistant~}}
    {{gen 'answer' temperature=0 max_tokens=500}}
    {{~/assistant}}
    '''

    SOLUTION_PROMPT = '''
    {{#system~}} You are a helpful and terse AI assistant{{~/system}}

    {{#user~}}
    Read the following conversation:
    {{messages}}
    Now generate the final solution to the User's query.
    {{~/user}}

    {{#assistant~}}
    {{gen 'answer' temperature=0 max_tokens=500}}
    {{~/assistant}}
    '''

    def __init__(self,
                 agents: Tuple[AssistantAgent],
                 messages: List[Any] | None = None,
                 termination_message: str = 'TERMINATE SUCCESSFULLY',
                 error_message: str = 'ERROR',
                 mode: str = 'BROADCAST',
                 rounds: int = 5,
                 round_robin: bool = True,
                 llm=None,
                 memory=None,
                 async_mode=False,
                 debug_mode=False):

        if messages is None:
            messages = []

        self.debug_mode = debug_mode

        if not any([isinstance(agent, AssistantAgent)
                    for agent in agents]):
            self.DEFAULT_PROMPT = self.DEFAULT_PROMPT[:self.DEFAULT_PROMPT.find(
                '{{~/system}}')] + '\nNote, User is also a participant, you can choose User.' + self.DEFAULT_PROMPT[self.DEFAULT_PROMPT.find('{{~/system}}'):]
        else:
            self.DEFAULT_PROMPT = self.DEFAULT_PROMPT[:self.DEFAULT_PROMPT.find(
                '{{~/system}}')] + '\nNote, User is not a participant, you cannot choose User.' + self.DEFAULT_PROMPT[self.DEFAULT_PROMPT.find('{{~/system}}'):]
        self.engine = engine(
            self.DEFAULT_PROMPT, llm=llm, memory=memory, async_mode=async_mode)
        self.solution_summarizer = engine(
            self.SOLUTION_PROMPT, llm=llm, memory=memory, async_mode=async_mode)

        self.agents = agents
        self.agent_dict = {agent.name: agent for agent in agents}
        self.messages = messages
        self.termination_message = termination_message
        self.error_message = error_message
        self.mode = mode
        self.rounds = rounds
        self.round_robin = round_robin
        self.current_agent = 0  # Used to keep track of next agent in sequence

    @property
    def agent_string(self):
        """
        Returns a string representation of all the agent names separated by commas.
        """
        return '\n\n'.join([f'NAME: {agent.name}\n DESC: {agent.description}' for agent in self.agents])

    def run_sequence(self, context):
        """
        Runs the sequence of agents in the multi-agent system.

        Args:
            context: The context for the current round.

        Returns:
            A list of messages exchanged between agents during the sequence.
        """
        self.messages.append(['User', context])
        while self.rounds != 0 and not self._termination_message_received():
            if self.debug_mode:
                print(
                    f'{"-"*5}Messaging next agent : {self.agents[self.current_agent].name}{"-"*5}\n\n')

            self._message_next_agent()

            if self.debug_mode:
                print(f'{self.messages[-1][0]}\n\n{self.messages[-1][1]}')

            if self.current_agent == 0 and not self.round_robin:
                break

            self.rounds -= 1
        return self.messages

    async def a_run_sequence(self, context):
        """
        Runs the sequence of agents in the multi-agent system in async.

        Args:
            context: The context for the current round.

        Returns:
            A list of messages exchanged between agents during the sequence.
        """
        self.messages.append(['User', context])
        while self.rounds != 0 and not self._termination_message_received():
            if self.debug_mode:
                print(
                    f'{"-"*5}Messaging next agent : {self.agents[self.current_agent].name}{"-"*5}\n\n')

            await self._a_message_next_agent()
            if self.debug_mode:
                print(
                    f'{self.messages[-1][0]}\n\n{self.messages[-1][1]}')

            if self.current_agent == 0 and not self.round_robin:
                break

            self.rounds -= 1
        return self.messages

    def run_auto(self, context):
        """
        Runs the multi-agent manager in auto mode.

        Args:
            context: The context for the multi-agent manager.

        Returns:
            A list containing the messages exchanged between agents and the final solution.
        """
        self.messages.append(['User', context])
        while self.rounds != 0 and not self._termination_message_received():
            next_agent = self._choose_next_agent()
            if self.debug_mode:
                print(
                    f'{"-" * 5}Messaging next agent : {next_agent.name}{"-" * 5}\n\n')

            self._message_next_agent(next_agent)
            if self.debug_mode:
                print(
                    f'{self.messages[-1][0]}\n\n{self.messages[-1][1]}')

            self.rounds -= 1
        final_solution = self.solution_summarizer(
            messages=self._parse_messages()).get('answer')

        if self.debug_mode:
            print(final_solution)

        return [self.messages, final_solution]

    async def _a_message_next_agent(self, next_agent=None):
        """
        Sends a message to the next agent in the list and receives a response.

        Args:
            next_agent (Agent, optional): The next agent to send the message to. If not provided,
                the next agent in the list will be selected. Defaults to None.

        Returns:
            None
        """
        if next_agent is None:
            next_agent = self.agents[self.current_agent]
            self.current_agent = (self.current_agent + 1) % len(self.agents)

        if next_agent.async_mode:
            received_message = await next_agent.a_receive(
                self.agent_string, self._parse_messages(), self.termination_message)
        else:
            received_message = next_agent.receive(
                self.agent_string, self._parse_messages(), self.termination_message)

        self.messages.append([next_agent.name, received_message])

    def _message_next_agent(self, next_agent=None):
        """
        Sends a message to the next agent in the sequence and receives a response.

        Args:
            next_agent (Agent, optional): The next agent to send the message to. If None, the next agent in the sequence is used.

        Returns:
            None
        """

        if next_agent is None:
            next_agent = self.agents[self.current_agent]
            self.current_agent = (self.current_agent + 1) % len(self.agents)

        assert not next_agent.async_mode, "Don't use run_sequence for async agents, use a_run_sequence instead"

        received_message = next_agent.receive(
            self.agent_string, self._parse_messages(), self.termination_message)

        self.messages.append([next_agent.name, received_message])

    def _termination_message_received(self):
        """
        Checks if the termination message is present in the last received message.

        Returns:
            bool: True if the termination message is present, False otherwise.
        """
        return self.termination_message in self.messages[-1][1]

    def _parse_messages(self):
        """
        Parses the messages stored in the `self.messages` list and returns a formatted string.

        Returns:
            str: A formatted string containing the parsed messages.
        """
        return f'\n\n{"-"*20}'.join([f'{index}) {message[0]}\n{message[1]}' for index, message in enumerate(self.messages)])

    def _choose_next_agent(self):
        """
        Chooses the next agent based on the output of the engine.

        Returns:
            The next agent to be used.

        """
        output = self.engine(agents=self.agent_string,
                             messages=self._parse_messages())
        if self.debug_mode:
            print(f"Chosen next agent as {output.get('answer')}")
        return self.agent_dict[output.get('answer')]
