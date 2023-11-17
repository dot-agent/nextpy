import pytest
from unittest.mock import MagicMock, patch
from openagent.agent.base_agent import BaseAgent, AgentState
from openagent.tools.basetool import BaseTool
from openagent.memory.base import BaseMemory

class MockBaseTool(BaseTool):
    # Assuming BaseTool does not have any mandatory methods
    pass

class MockMemory(BaseMemory):
    def add_memory(self, prompt: str, llm_response: str) -> None:
        self.messages.append({'prompt': prompt, 'response': llm_response})

    def get_memory(self, **kwargs) -> str:
        return "\n".join(m['prompt'] for m in self.messages)

    def remove_memory(self, prompt: str) -> None:
        self.messages = [m for m in self.messages if m['prompt'] != prompt]

    def clear(self) -> None:
        self.messages.clear()

@pytest.fixture
def base_agent_obj():
    tools = [
        MockBaseTool(name="MockTool1", description="Mock description for tool 1"),
        MockBaseTool(name="MockTool2", description="Mock description for tool 2")
    ]
    memory = MockMemory()
    agent = BaseAgent(
        knowledgebase=MagicMock(), 
        tools=tools, 
        llm=MagicMock(), 
        prompt_template="Test Prompt", 
        input_variables={"knowledge_variable": "knowledge_variable"},
        agent_id="Test Agent", 
        memory=memory, 
        caching=True, 
        output_key="Test Output", 
        return_complete=False
    )
    yield agent  # use yield to ensure cleanup after tests have run

def test_init_with_tools(base_agent_obj):
    assert len(base_agent_obj.tools) == 2
    assert base_agent_obj.state == AgentState.IDLE
    # assert base_agent_obj.get_knowledge_variable == "Test"

def test_add_tool(base_agent_obj):
    new_tool = MockBaseTool(name="MockTool3", description="Mock description for tool 3")
    base_agent_obj.add_tool(new_tool)
    assert len(base_agent_obj.tools) == 3
    assert new_tool in base_agent_obj.tools

def test_remove_tool(base_agent_obj):
    tool = base_agent_obj.tools[0]
    base_agent_obj.remove_tool(tool)
    assert len(base_agent_obj.tools) == 1
    assert tool not in base_agent_obj.tools

# @patch('openagent.agent.base_agent.compiler')
# def test_run(mock_compiler, base_agent_obj):
#     # Set up the mock compiler's return value to simulate a callable that returns a mock object
#     mock_output = MagicMock()
#     mock_output.variables.return_value = {'Test Output': 'Test Result'}
#     mock_output.__getitem__.return_value = 'Test Result'  # Mock the dictionary access
#     mock_compiler.return_value = MagicMock(return_value=mock_output)
    
#     # Call the method under test
#     result = base_agent_obj.run(knowledge_variable='Test Knowledge')
    
#     # Check the result is not none and correct value returned
#     assert result is not None
#     assert result == 'Test Result'

# TODO: Figure out async related errors
# @pytest.mark.asyncio
# @patch('openagent.agent.base_agent.compiler')
# async def test_arun(mock_compiler, base_agent_obj):
#     # Set up the mock compiler's return value
#     mock_output = MagicMock()
#     mock_output.variables.return_value = {'Test Output': 'Test Result'}
#     mock_output.__getitem__.return_value = 'Test Result'
#     mock_compiler.return_value = MagicMock(return_value=mock_output)
    
#     # Call the method under test with await
#     result = await base_agent_obj.arun(knowledge_variable='Test Knowledge')
    
#     # Assert the expected result
#     assert result is not None
#     assert result == 'Test Result'

def test_get_knowledge(base_agent_obj):
    base_agent_obj.knowledgebase.retrieve_data.return_value = ['doc1', 'doc2', 'doc3']
    knowledge = base_agent_obj.get_knowledge('Test Query')
    base_agent_obj.knowledgebase.retrieve_data.assert_called_once_with('Test Query')
    assert knowledge == 'doc1doc2doc3'