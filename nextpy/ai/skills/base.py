# base class for all skills
from typing import Callable, Optional, Type
from abc import ABC
from pydantic import BaseModel


class BaseSkill(ABC, BaseModel):

    name: str
    # The unique name of the tool that clearly communicates its purpose.
    description: str
    # Used to tell the model how/when/why to use the tool.You can provide few-shot examples as a part of the description.
    func: Callable = None
    # Function which acts as a tool and takes in input
    args_schema: Optional[Type[BaseModel]] = None
    # Pydantic model class to validate and parse the tool's input arguments
    return_direct: bool = False
    # Whether to return the tool's output directly. Setting this to True means that after the tool is called, the AgentExecutor will stop looping.
    verbose: bool = False
    # Whether to log the tool's progress.
