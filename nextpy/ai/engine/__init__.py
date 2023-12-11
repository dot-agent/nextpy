import types
import sys
import os
import requests
from . import library as commands
from ._program import Program
from . import llms

from ._utils import load, chain
from . import selectors
import nest_asyncio
import asyncio

# the user needs to set an LLM before they can use engine
llm = None


# This makes the engine module callable
class Engine(types.ModuleType):
    def __call__(
        self,
        template,
        llm=None,
        cache_seed=0,
        logprobs=None,
        silent=None,
        async_mode=False,
        stream=None,
        caching=None,
        await_missing=False,
        logging=False,
        **kwargs
    ):
        return Program(
            template,
            llm=llm,
            cache_seed=cache_seed,
            logprobs=logprobs,
            silent=silent,
            async_mode=async_mode,
            stream=stream,
            caching=caching,
            await_missing=await_missing,
            logging=logging,
            **kwargs
        )


sys.modules[__name__].__class__ = Engine


def load(engine_file):
    """Load a engine program from the given text file.

    If the passed file is a valid local file it will be loaded directly.
    Otherwise, if it starts with "http://" or "https://" it will be loaded
    from the web.
    """

    if os.path.exists(engine_file):
        with open(engine_file, "r") as f:
            template = f.read()
    elif engine_file.startswith("http://") or engine_file.startswith("https://"):
        template = requests.get(engine_file).text
    else:
        raise ValueError("Invalid engine file: %s" % engine_file)

    return sys.modules[__name__](template)