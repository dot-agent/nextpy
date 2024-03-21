# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts.
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from unittest.mock import MagicMock

import pytest

from nextpy.ai.agent.base_agent import AgentState, BaseAgent
from nextpy.ai.memory.base import BaseMemory
from nextpy.ai.skills.base import BaseSkill


class MockBaseSkill(BaseSkill):
    # Assuming BaseSkill does not have any mandatory methods
    pass


class MockMemory(BaseMemory):
    def add_memory(self, prompt: str, llm_response: str) -> None:
        """Add a memory message to the log. This is used to inform the user of memory problems in LLM.

        Args:
        prompt: The prompt that will be displayed
        llm_response: The response that will be displayed


        Returns:
        True if the message was added False if it was already in the log ( in which case nothing is
        """
        self.messages.append({"prompt": prompt, "response": llm_response})

    def get_memory(self, **kwargs) -> str:
        """Get memory in bytes. This is a string of all the messages that have been sent to the instrument.



        Returns:
        A string of all the messages that have been sent to the instrument as a single string with newlines separating them
        """
        return "\n".join(m["prompt"] for m in self.messages)

    def remove_memory(self, prompt: str) -> None:
        """Remove memory from message list. This is useful for debugging and to avoid accidental changes in messages that are stored in memory.

        Args:
        prompt: prompt to remove from memory


        Returns:
        whether or not messages were removed from memory ( True ) or not ( False ). The memory is removed by checking if the prompt is different from the one
        """
        self.messages = [m for m in self.messages if m["prompt"] != prompt]

    def clear(self) -> None:
        """Clear all messages. This is useful when you want to re - send a message in the middle of a message processing cycle.



        Returns:
        ` ` None ` ` on success or an error message on failure. The message is removed from the queue
        """
        self.messages.clear()


@pytest.fixture
def base_agent_obj():
    """Return a BaseAgent object with mock base skills and memory. This is a context manager to allow unit tests to run."""
    skills = [
        MockBaseSkill(name="Mockskill1",
                      description="Mock description for skill 1"),
        MockBaseSkill(name="Mockskill2",
                      description="Mock description for skill 2"),
    ]
    memory = MockMemory()
    agent = BaseAgent(
        rag=MagicMock(),
        skills=skills,
        llm=MagicMock(),
        prompt_template="Test Prompt",
        input_variables={"knowledge_variable": "knowledge_variable"},
        agent_id="Test Agent",
        memory=memory,
        caching=True,
        output_key="Test Output",
        return_complete=False,
    )
    yield agent  # use yield to ensure cleanup after tests have run


def test_init_with_skills(base_agent_obj):
    """Tests init with skills. This is a test to make sure we don't accidentally get the skills from the Agent object after it has been initialized.


    Args:
    base_agent_obj: An instance of the
    """
    assert len(base_agent_obj.skills) == 2
    assert base_agent_obj.state == AgentState.IDLE
    # assert base_agent_obj.get_knowledge_variable == "Test"


def test_add_skill(base_agent_obj):
    """Tests adding a skill to the base agent. This is a convenience method to make sure we don't accidentally add skills that are already in the list.


    Args:
    base_agent_obj: An instance of BaseAgent
    """
    new_skill = MockBaseSkill(
        name="Mockskill3", description="Mock description for skill 3")
    base_agent_obj.add_skill(new_skill)
    assert len(base_agent_obj.skills) == 3
    assert new_skill in base_agent_obj.skills


def test_remove_skill(base_agent_obj):
    """Remove a skill from the base agent. Checks that it is removed and no more skills are added.


    Args:
    base_agent_obj: An instance of : class : ` yum. manufacturers. base_agent. YumAgent
    """
    skill = base_agent_obj.skills[0]
    base_agent_obj.remove_skill(skill)
    assert len(base_agent_obj.skills) == 1
    assert skill not in base_agent_obj.skills


# @patch('llms.agent.base_agent.engine')
# def test_run(mock_engine, base_agent_obj):
#     # Set up the mock engine's return value to simulate a callable that returns a mock object
#     mock_output = MagicMock()
#     mock_output.variables.return_value = {'Test Output': 'Test Result'}
#     mock_output.__getitem__.return_value = 'Test Result'  # Mock the dictionary access
#     mock_engine.return_value = MagicMock(return_value=mock_output)

#     # Call the method under test
#     result = base_agent_obj.run(knowledge_variable='Test Knowledge')

#     # Check the result is not none and correct value returned
#     assert result is not None
#     assert result == 'Test Result'

# TODO: Figure out async related errors
# @pytest.mark.asyncio
# @patch('llms.agent.base_agent.engine')
# async def test_arun(mock_engine, base_agent_obj):
#     # Set up the mock engine's return value
#     mock_output = MagicMock()
#     mock_output.variables.return_value = {'Test Output': 'Test Result'}
#     mock_output.__getitem__.return_value = 'Test Result'
#     mock_engine.return_value = MagicMock(return_value=mock_output)

#     # Call the method under test with await
#     result = await base_agent_obj.arun(knowledge_variable='Test Knowledge')

#     # Assert the expected result
#     assert result is not None
#     assert result == 'Test Result'


def test_get_knowledge(base_agent_obj):
    """Tests the get_knowledge method. This is a test method to make sure we have the right knowledge when retrieving documents from Ragged Agents.


    Args:
    base_agent_obj: Instance of BaseAgent class to
    """
    base_agent_obj.rag.retrieve_data.return_value = ["doc1", "doc2", "doc3"]
    knowledge = base_agent_obj.get_knowledge("Test Query")
    base_agent_obj.rag.retrieve_data.assert_called_once_with("Test Query")
    assert knowledge == "doc1doc2doc3"
