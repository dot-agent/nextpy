import yaml
from openagent import compiler
from openagent.llms._openai import OpenAI
from openagent.agent.chat import ChatAgent
from openagent.vectorstores.chroma import Chroma
from openagent.text_splitter import CharacterTextSplitter
from openagent.knowledgebase.document_loaders.file.base import SimpleDirectoryReader
from openagent.knowledgebase.base import SimpleKnowledgeBase
from openagent.vectorstores.embeddings.openai import OpenAIEmbeddings
from textwrap import indent
from importlib import import_module


def load_agent_config(config_path: str) -> ChatAgent:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Load the components of the agent from the configuration
    llm_config = config['llm']
    llm = OpenAI(model=llm_config['model'])

    kb_config = config['knowledgebase']
    data_loader = SimpleDirectoryReader(kb_config['data_source'])
    raw_data = data_loader.load_data(**kb_config.get('data_loader_args', {}))
    data_transformer = CharacterTextSplitter(chunk_overlap=kb_config['data_transformer']['chunk_overlap'], chunk_size=kb_config['data_transformer']['chunk_size'])
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma(embedding_function=embeddings)
    knowledgebase = SimpleKnowledgeBase(raw_data=raw_data, data_transformer=data_transformer, vector_store=vector_store)

    agent_config = config['agent']
    agent = ChatAgent(
        llm=llm,
        prompt_template=agent_config['prompt_template'],
        input_variables=agent_config['input_variables'],
        knowledgebase=knowledgebase,
        output_key=agent_config['output_key']
    )

    return agent

def export_agent_config(agent, data_loader, data_transformer, vector_store, llm, config_path):
    config = {
        'llm': {
            'type': f"{llm.__class__.__name__}",
            'model': llm.model
        },
        'knowledgebase': {
            'data_source': data_loader.data_source,
            'data_loader': f"{data_loader.__class__.__name__}",
            'data_transformer': {
                'type': f"{data_transformer.__class__.__name__}",
                'chunk_overlap': data_transformer._chunk_overlap,
                'chunk_size': data_transformer._chunk_size
            },
            'vector_store': {
                'type': f"{vector_store.__class__.__name__}",
                'embedding_function': f"{vector_store.embedding_function.__class__.__name__}"
            }
        },
        'agent': {
            'type': f"{agent.__class__.__name__}",
            'prompt_template': agent.prompt_template,
            'input_variables': agent.input_variables,
            'output_key': agent.output_key
        }
    }

    with open(config_path, 'w') as f:
        yaml.safe_dump(config, f)
