from typing import Any

from pydantic import BaseModel

from nextpy.ai.memory import BaseMemory


class SimpleMemory(BaseMemory, BaseModel):
    def add_memory(self, prompt: str, llm_response: Any) -> None:
        """Add a self-created message to the store."""
        unique = True
        for conversation in self.messages:
            if (
                conversation["prompt"] == prompt
                and conversation["llm_response"] == llm_response
            ):
                unique = False
        if unique:
            self.messages.append({"prompt": prompt, "llm_response": llm_response})

    def get_memory(self, **kwargs) -> str:
        """Retrieve entire memory from the store."""
        if len(self.messages) != 0:
            messages_to_text = "Current conversation:\n"
            for conversation in self.messages:
                messages_to_text = (
                    messages_to_text
                    + "Human: "
                    + conversation["prompt"]
                    + "\n"
                    + "AI: "
                    + conversation["llm_response"]
                    + "\n"
                )
        else:
            messages_to_text = ""
        return messages_to_text

    def remove_memory(self, prompt: str) -> None:
        """Remove a memory from the store."""
        for conversation in self.messages:
            if conversation["prompt"] == prompt:
                self.messages.remove(conversation)
                break

    def clear(self) -> None:
        """Clear all memories."""
        self.messages.clear()
