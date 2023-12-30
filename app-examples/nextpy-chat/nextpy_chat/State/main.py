# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import os
from openai import OpenAI
import nextpy as xt 
from .state import State, QA

from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key = os.environ["OPENAI_API_KEY"]
)

DEFAULT_CHATS = {
    "Intros": [],
}

class MainState(State):
    """The nextpy_chat main page state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    # Whether the drawer is open.
    drawer_open: bool = False

    # Whether the modal is open.
    modal_open: bool = False

    # QA message index for current chat
    index : dict[str, int] = { current_chat:0 }

    # Display welcome message 
    display_val: str = 'visible'


    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []
        self.index[self.new_chat_name] = 0
        # Toggle the modal.
        self.modal_open = False

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        """Toggle the drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]
        self.index[self.current_chat] = 0
        self.display_val = 'visible'
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name
        self.toggle_drawer()

    def toggle_like(self, index):
        if self.chats[self.current_chat][index].like_bg=='white' :
            self.chats[self.current_chat][index].like_bg='purple'
        else :
            self.chats[self.current_chat][index].like_bg='white'

    def toggle_dislike(self, index):
        if self.chats[self.current_chat][index].dislike_bg=='white':
            self.chats[self.current_chat][index].dislike_bg='purple'
        else :
            self.chats[self.current_chat][index].dislike_bg='white'

    def open_interview_prep(self):
        pass 

    @xt.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        self.display_val = 'none'

        # Check if the question is empty
        if self.question == "":
            return

        # Add the question to the list of questions.
        qa = QA(question=self.question, answer="", index=self.index[self.current_chat])
        self.index[self.current_chat] += 1
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        self.question = ""
        yield

        # Build the messages.
        messages = [
            {"role": "system", "content": "You are a friendly chatbot named NextpyGPT."}
        ]
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = messages[:-1]

        # Start a new session to answer the question.
        session = client.chat.completions.create(
            model=os.getenv("OPENAI_API_MODEL", "gpt-4-1106-preview"),
            messages=messages,
            stream=True,
        )

        # Stream the results, yielding after every word.
        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                answer_text = item.choices[0].delta.content
                if answer_text is None:
                    answer_text = ""  # assign empty string if answer_text was None
                self.chats[self.current_chat][-1].answer += answer_text
                self.chats = self.chats
                yield

        # Toggle the processing flag.
        self.processing = False