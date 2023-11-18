from __future__ import annotations

"""Base implementation for tools or skills."""

import warnings
from abc import ABC, abstractmethod
from inspect import signature
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

from pydantic import (
    BaseModel,
    create_model,
    root_validator,
    validate_arguments,
)


def _get_filtered_args(
    inferred_model: Type[BaseModel],
    func: Callable,
) -> dict:
    """Get the arguments from a function's signature."""
    schema = inferred_model.schema()["properties"]
    valid_keys = signature(func).parameters
    return {k: schema[k] for k in valid_keys if k != "run_manager"}

def _create_subset_model(
    name: str, model: BaseModel, field_names: list
) -> Type[BaseModel]:
    """Create a pydantic model with only a subset of model's fields."""
    fields = {}
    for field_name in field_names:
        field = model.__fields__[field_name]
        fields[field_name] = (field.type_, field.field_info)
    return create_model(name, **fields)  # type: ignore

def create_schema_from_function(
    model_name: str,
    func: Callable,
) -> Type[BaseModel]:
    """
        model_name: Name to assign to the generated pydandic schema
        func: Function to generate the schema from
    """
    validated = validate_arguments(func, config=_SchemaConfig)  # type: ignore
    inferred_model = validated.model  # type: ignore
    if "run_manager" in inferred_model.__fields__:
        del inferred_model.__fields__["run_manager"]
    # Pydantic adds placeholder virtual fields we need to strip
    valid_properties = _get_filtered_args(inferred_model, func)
    return _create_subset_model(
        f"{model_name}Schema", inferred_model, list(valid_properties)
    )


class BaseTool(ABC, BaseModel):
  # Interface openams tools must implement.

    name: str
    #The unique name of the tool that clearly communicates its purpose.
    description: str
    #Used to tell the model how/when/why to use the tool.You can provide few-shot examples as a part of the description.
    func: Callable = None
    #Function which acts as a tool and takes in input
    args_schema: Optional[Type[BaseModel]] = None
    #Pydantic model class to validate and parse the tool's input arguments
    return_direct: bool = False
    # Whether to return the tool's output directly. Setting this to True means that after the tool is called, the AgentExecutor will stop looping.
    verbose: bool = False
    #Whether to log the tool's progress.

    @property
    def is_single_input(self) -> bool:
        """Whether the tool only accepts a single input."""
        keys = {k for k in self.args if k != "kwargs"}
        return len(keys) == 1

    @property
    def args(self) -> dict:
        if self.args_schema is not None:
            return self.args_schema.schema()["properties"]
        else:
            schema = create_schema_from_function(self.name, self.run)
            return schema.schema()["properties"]

    def _parse_input(
        self,
        tool_input: Union[str, Dict],
    ) -> Union[str, Dict[str, Any]]:
        input_args = self.args_schema
        if isinstance(tool_input, str):
            if input_args is not None:
                key_ = next(iter(input_args.__fields__.keys()))
                input_args.validate({key_: tool_input})
            return tool_input
        else:
            if input_args is not None:
                result = input_args.parse_obj(tool_input)
                return {k: v for k, v in result.dict().items() if k in tool_input}
        return tool_input

    @root_validator()
    def raise_deprecation(cls, values: Dict) -> Dict:
        """Raise deprecation warning if callback_manager is used."""
        if values.get("callback_manager") is not None:
            warnings.warn(
                "callback_manager is deprecated. Please use callbacks instead.",
                DeprecationWarning,
            )
            values["callbacks"] = values.pop("callback_manager", None)
        return values

    @abstractmethod
    def run(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Use the tool.
        """

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        if isinstance(tool_input, str):
            return (tool_input,), {}
        else:
            return (), tool_input

    def run(self,tool_input: Union[str, Dict], verbose: Optional[bool] = None,**kwargs: Any) -> Any:
        """Parses the output and checks if the input is string and handles exceptions"""
        parsed_input = self._parse_input(tool_input)

        observation = self.run(parsed_input)

        return observation

        # if isinstance(parsed_input, str):
        #     raise Exception("Tool input should be string")
        # else:
        #     return parsed_input

class ExceptionTool(BaseTool):
    name = "_Exception"
    description = "Exception tool"

    def run(
        self,
        query: str,
    ) -> str:
        return query
    
class InvalidTool(BaseTool):
    """Tool that is run when invalid tool name is encountered by agent."""

    name = "invalid_tool"
    description = "Called when tool name is invalid."

    def run(
        self, tool_name: str,
    ) -> str:
        """Use the tool."""
        return f"{tool_name} is not a valid tool, try another one."

class Tool(BaseTool):
    """Tool that takes in function or coroutine directly."""

    class Config:
        arbitrary_types_allowed = True

    def args(self) -> dict:
        """The tool's input arguments."""
        if self.args_schema is not None:
            return self.args_schema.schema()["properties"]
        # For backwards compatibility, if the function signature is ambiguous,
        # assume it takes a single string input.
        return {"tool_input": {"type": "string"}}
    
    def run(self, tool_input, **kwargs: Any) -> Any:
        """Actually calls the tool and gives output."""
        try:
            return (self.func(tool_input, **kwargs))
        except Exception as e:
            return e

    def __call__(self, tool_input: str, **kwargs) -> str:
        """Make tool callable."""
        # try:
        #     parsed_input = self.run(tool_input , **kwargs)
        # except Exception as e:
        #     return e
        # final_result =  self.run(tool_input=parsed_input, **kwargs)
        # return final_result