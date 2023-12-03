import pytest
from pydantic import ValidationError
from openams.agent.config import create_config, base_config

# Test Data
test_data = [
    ("write_json_file", "Write a JSON file to the filesystem", {"fname": {"type": "string", "description": "The name of the file to write"}, "json_str": {"type": "string", "description": "The JSON content of the file to write"}}, ["fname", "json_str"]),
    ("write_yml_file", "Write a YAML file to the filesystem", {"fname": {"type": "string", "description": "The name of the file to write"}, "yaml_str": {"type": "string", "description": "The YAML content of the file to write"}}, ["fname", "yaml_str"]),
    ("write_innovation_file", "Write a custom file to the filesystem", {"content": {"type": "string", "description": "The content of the file to write"}}, ["content"])
]

@pytest.mark.parametrize("name, description, properties, required_fields", test_data)
def test_create_config(name, description, properties, required_fields):
    config = create_config(
        name=name,
        description=description,
        properties=properties,
        required_fields=required_fields,
        base_config=base_config
    )

    # Basic structure assertions
    assert 'functions' in config
    assert isinstance(config['functions'], list)
    assert len(config['functions']) == 1

    function_config = config['functions'][0]

    # Assertions to check if the configuration is correctly formed
    assert function_config['name'] == name
    assert function_config['description'] == description
    assert all(item in function_config['properties'] for item in properties)
    assert function_config['required'] == required_fields

    # Check the types of properties
    for prop in properties:
        assert function_config['properties'][prop]['type'] == properties[prop]['type']

    # Check for base configuration inheritance
    assert config['use_cache'] == base_config['use_cache']
    assert config['temperature'] == base_config['temperature']
    assert config['config_list'] == base_config['config_list']
    assert config['request_timeout'] == base_config['request_timeout']

# def test_invalid_configuration():
#     with pytest.raises(ValidationError):
#         create_config(
#             name="invalid_config",
#             description="",
#             properties={
#                 "invalid_prop": {
#                     "type": 123,  # Providing an integer instead of a string, assuming 'type' should be a string
#                     "description": "Invalid property for testing"
#                 }
#             },
#             required_fields=["invalid_prop"],
#             base_config=base_config
#         )



def test_empty_configuration():
    # Empty configurations should still work
    empty_config = create_config(
        name="empty_config",
        description="Empty configuration for testing",
        properties={},
        required_fields=[],
        base_config=base_config
    )

    assert empty_config['functions'][0]['name'] == "empty_config"
    assert not empty_config['functions'][0]['properties']  # Should be empty
    assert not empty_config['functions'][0]['required']  # Should be empty


