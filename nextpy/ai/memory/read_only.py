# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from typing import Any, List

from nextpy.ai.memory.base import BaseMemory


class ReadOnlyMemory(BaseMemory):
    """Read-only memory class wrapper that prevents modification."""

    memory: BaseMemory

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
            prompts.append(conversation["prompt"])

        return prompts
