from typing import Any, Callable, Coroutine, Dict, List
import re
import inspect


class StateManager:
    ''' FSM that handles the workflow '''

    def __init__(self, agents: Dict[str, Any], states: Dict[int, List['Handler']], initial_state: int):
        self.states = states
        self.current_state = initial_state
        self.agents = agents
        self.action_queue = []
        self.context = {}

    async def submit_action(self, function, *args, **kwargs):
        """Start the workflow with the specified agent and arguments.


        Args:
            agent: The agent to start the workflow with.
            *args: Variable length arguments.
            **kwargs: Keyword arguments.
        """
        self.queue_action(function, *args, **kwargs)

        while self.current_state != -1 and len(self.action_queue) > 0:
            responses = []

            # check if func is async, if it is then await it, otherwise call it
            while len(self.action_queue) > 0:
                func, args, kwargs = self.action_queue.pop(0)
                if inspect.iscoroutinefunction(func):
                    responses.append(await func(*args, **kwargs))
                else:
                    responses.append(func(*args, **kwargs))

            for response in responses:
                for handler in self.states[self.current_state]:
                    if handler.check_update(response):
                        new_state = await handler.handle_update(self, response)
                        self.current_state = new_state if new_state is not None else self.current_state
                        break

    def queue_action(self, action, *args, **kwargs):
        self.action_queue.append((action, args, kwargs))


class Handler:
    def __init__(self, callback: Callable[[StateManager, Any], Coroutine[Any, Any, int]], pattern):
        self._callback = callback  # callback is a coroutine function
        self._pattern = pattern  # pattern can be a regex pattern or a callable function

    def check_update(self, response):
        if callable(self._pattern):
            return self._pattern(response)
        elif isinstance(self._pattern, re.Pattern):
            return self._pattern.match(response) is not None
        elif isinstance(self._pattern, str):
            regex = re.compile(self._pattern)
            return regex.match(response) is not None
        return False

    async def handle_update(self, workflow: StateManager, response):
        return await self._callback(workflow, response)
