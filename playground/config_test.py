import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
openagent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(openagent_dir)


import pytest
from openagent.agent._config import export_agent_config, load_agent_config
from openagent.agent.chat import ChatAgent
from openagent.llms._openai import OpenAI
from openagent.vectorstores.chroma import Chroma
from openagent.text_splitter import CharacterTextSplitter
from openagent.knowledgebase.document_loaders.file.base import SimpleDirectoryReader
from openagent.knowledgebase.base import SimpleKnowledgeBase
from openagent.vectorstores.embeddings.openai import OpenAIEmbeddings

def test_agent_config():

    # Initialize your agent
    llm = OpenAI(model='gpt-3.5-turbo')
    data_source = './test_data/meteoric' 
    data_loader = SimpleDirectoryReader(data_source)
    raw_data = SimpleDirectoryReader(data_source).load_data()
    data_transformer = CharacterTextSplitter(chunk_overlap=40, chunk_size=1024)
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(embedding_function=embeddings)
    knowledgebase = SimpleKnowledgeBase(raw_data=raw_data, data_transformer=data_transformer, vector_store=vector_store)

    chat_template = '''
                {{#user~}}
                You will use this FORMAT only to answer user's QUERY
                FORMAT: {{format}}
                QUERY: {{input}}

                Use the below knowledge to answer QUERY in given FORMAT:-
                {{RETRIEVED_KNOWLEDGE}}
                {{~/user}}

                {{#assistant~}}
                Yes, I will tell you about with that
                {{~/assistant}}

                {{#user~}}
                Yes, tell me
                {{~/user}}

                {{#assistant~}}
                {{gen 'response' temperature=0 max_tokens=300}}
                {{~/assistant}}'''

    agent = ChatAgent(
        llm=llm,
        prompt_template=chat_template,
        input_variables={"knowledge_variable": 'input', "extras": 'format'},
        knowledgebase=knowledgebase,
        output_key='response'
        )

    # Export the agent config
    config_path = 'agent_config.yaml'
    export_agent_config(agent, config_path)

    # Load the agent config
    loaded_agent = load_agent_config(config_path)

    # Compare the properties of the original agent and the loaded agent
    assert agent.llm.model == loaded_agent.llm.model
    assert agent.prompt_template == loaded_agent.prompt_template
    assert agent.input_variables == loaded_agent.input_variables
    assert agent.output_key == loaded_agent.output_key

    # Compare the properties of the original agent and the loaded agent
    print("Checking LLM model...")
    assert agent.llm.model == loaded_agent.llm.model
    print("LLM model check passed")

    print("Checking prompt template...")
    assert agent.prompt_template == loaded_agent.prompt_template
    print("Prompt template check passed")

    print("Checking input variables...")
    assert agent.input_variables == loaded_agent.input_variables
    print("Input variables check passed")

    print("Checking output key...")
    assert agent.output_key == loaded_agent.output_key
    print("Output key check passed")

    # Add more assertions as needed to test the properties of your agent
