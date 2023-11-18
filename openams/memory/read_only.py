from typing import Any, List

from openams.memory.base import BaseMemory

class ReadOnlyMemory(BaseMemory):
    """Read-only memory class wrapper that prevents modification."""
    memory: BaseMemory

    def __init__(self, memory: BaseMemory):
        self.memory = memory

    def add_memory(self, prompt: str, llm_response: Any) -> None:
        """cannot edit a read only memory."""
        pass

    def get_memory(self, **kwargs) -> Any:
        """Retrieve entire memory from the store."""
        return self.memory.get_memory(**kwargs)

    def remove_memory(self, prompt: str) -> None:
        """cannot edit a read only memory."""
        pass

    def clear(self) -> None:
        """cannot edit a read only memory."""
        pass

    @property
    def memory_keys(self) -> List[str]:
        """Return the prompts for all memories."""
        prompts = []
        for conversation in self.memory.messages:
            prompts.append(conversation['prompt'])
        
        return prompts