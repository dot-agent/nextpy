import json
import importlib


class _ConfigManager:
    @staticmethod
    def export_config(agent, config_path):
        import json
        try:
            config = {
                'agent_id': agent.agent_id,
                'llm': {
                    'class': f"{agent.llm.__module__}.{agent.llm.__class__.__name__}",
                    'args': {'model': agent.llm.model_name}
                },
                'prompt_template': agent.prompt_template,
                'input_variables': agent.input_variables,
            }

            if agent.knowledgebase is not None:
                kb = agent.knowledgebase
                config['knowledgebase'] = {
                    'class': f"{kb.__module__}.{kb.__class__.__name__}",
                    'args': {
                        'raw_data': kb.raw_data,
                        'data_transformer': {
                            'class': f"{kb.data_transformer.__module__}.{kb.data_transformer.__class__.__name__}",
                            'args': {
                                'chunk_overlap': kb.data_transformer.chunk_overlap,
                                'chunk_size': kb.data_transformer.chunk_size,
                            },
                        },
                        'vector_store': {
                            'class': f"{kb.vector_store.__module__}.{kb.vector_store.__class__.__name__}",
                            'args': {
                                'embedding_function': {
                                    'class': f"{kb.vector_store.embedding_function.__module__}.{kb.vector_store.embedding_function.__class__.__name__}",
                                    'args': {},
                                },
                            },
                        },
                    },
                }

            with open(config_path, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error occurred while exporting config: {str(e)}")
            return False

        return True





    @classmethod
    def import_config(cls, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Initialize the arguments for the Agent constructor
        init_args = {}

        for key, value in config.items():
            if isinstance(value, dict) and 'class' in value:
                # If the value is a dict and contains a 'class' key, it represents a class instance
                class_ = cls.import_class(value['class'])
                args = value['args']

                # For args that represent class instances, import the class and create an instance
                for arg_key, arg_value in args.items():
                    if isinstance(arg_value, dict):
                        arg_class = cls.import_class(arg_value['class'])
                        arg_args = arg_value['args']
                        args[arg_key] = arg_class(**arg_args)

                # Create an instance of the class
                init_args[key] = class_(**args)
            else:
                # If the value is not a dict, or it's a dict but doesn't contain a 'class' key, it's a regular attribute
                init_args[key] = value

        return init_args

    @staticmethod
    def import_class(fully_qualified_name):
        parts = fully_qualified_name.split('.')
        module_name = '.'.join(parts[:-1])
        class_name = parts[-1]
        try:
            # Try to import the class from the module
            module = importlib.import_module(module_name)
            class_ = getattr(module, class_name)
        except ImportError:
            # If the import fails, try to get the class from the global scope
            class_ = globals().get(class_name)
            if class_ is None:
                raise AttributeError(f"module '{module_name}' has no attribute '{class_name}'")
        return class_
