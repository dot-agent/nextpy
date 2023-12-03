import autogen
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, List


class PropertyModel(BaseModel):
    type: str = Field(..., description="The data type of the property")
    description: str = Field(..., description="The description of the property")

class FunctionConfigModel(BaseModel):
    name: str = Field(..., description="Name of the function")
    description: str = Field(..., description="Description of the function")
    properties: Dict[str, PropertyModel] = Field(..., description="Parameters of the function")
    required: List[str] = Field(..., description="Required fields for the function parameters")


def create_config(name, description, properties, required_fields, base_config):
    # Validate the function configuration using Pydantic
    try:
        function_config = FunctionConfigModel(
            name=name,
            description=description,
            properties={key: PropertyModel(**value) for key, value in properties.items()},
            required=required_fields
        )
    except ValidationError as e:
        raise e  # This will ensure that a ValidationError is raised when the input is invalid

    # Merge with the base configuration and return
    return {
        **base_config,
        "functions": [function_config.dict()]
    }

# Base Configuration
base_config = {
    "use_cache": False,
    "temperature": 0,
    "config_list": autogen.config_list_from_models(["gpt-4"]),
    "request_timeout": 120,
}

# Configuration Definitions
run_sql_config = create_config(
    name="run_sql",
    description="Run a SQL query against the postgres database",
    properties={
        "sql": {
            "type": "string",
            "description": "The SQL query to run",
        }
    },
    required_fields=["sql"],
    base_config=base_config
)

write_file_config = create_config(
    name="write_file",
    description="Write a file to the filesystem",
    properties={
        "fname": {
            "type": "string",
            "description": "The name of the file to write",
        },
        "content": {
            "type": "string",
            "description": "The content of the file to write",
        },
    },
    required_fields=["fname", "content"],
    base_config=base_config
)

# Configuration for "write_json_file"
write_json_file_config = create_config(
    name="write_json_file",
    description="Write a JSON file to the filesystem",
    properties={
        "fname": {
            "type": "string",
            "description": "The name of the file to write",
        },
        "json_str": {
            "type": "string",
            "description": "The JSON content of the file to write",
        },
    },
    required_fields=["fname", "json_str"],
    base_config=base_config
)

# Configuration for "write_yaml_file"
write_yaml_file_config = create_config(
    name="write_yml_file",
    description="Write a YAML file to the filesystem",
    properties={
        "fname": {
            "type": "string",
            "description": "The name of the file to write",
        },
        "yaml_str": {
            "type": "string",
            "description": "The YAML content of the file to write",
        },
    },
    required_fields=["fname", "yaml_str"],
    base_config=base_config
)

# Configuration for "write_innovation_file"
write_innovation_file_config = create_config(
    name="write_innovation_file",
    description="Write a custom file to the filesystem",
    properties={
        "content": {
            "type": "string",
            "description": "The content of the file to write",
        },
    },
    required_fields=["content"],
    base_config=base_config
)
