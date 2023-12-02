import types
import sys
import os
import requests
from . import library as commands
from ._program import Program
from . import endpoints

from ._utils import load, merge_programs
from . import selectors
import nest_asyncio
import asyncio

# the user needs to set an LLM before they can use Engine
llm = None

# This makes the Engine module callable
class Engine(types.ModuleType):
    def __call__(self, template, llm=None, cache_seed=0, logprobs=None, silent=None, async_mode=False, stream=None, caching=None, await_missing=False, logging=False, memory=None, memory_threshold=1, **kwargs):
        return Program(template, llm=llm, cache_seed=cache_seed, logprobs=logprobs, silent=silent, async_mode=async_mode, stream=stream, caching=caching, await_missing=await_missing, logging=logging, memory=memory, memory_threshold=memory_threshold, **kwargs)
sys.modules[__name__].__class__ = Engine


def load(Engine_file):
    ''' Load a Engine program from the given text file.

    If the passed file is a valid local file it will be loaded directly.
    Otherwise, if it starts with "http://" or "https://" it will be loaded
    from the web.
    '''

    if os.path.exists(Engine_file):
        with open(Engine_file, 'r') as f:
            template = f.read()
    elif Engine_file.startswith('http://') or Engine_file.startswith('https://'):
        template = requests.get(Engine_file).text
    else:
        raise ValueError('Invalid Engine file: %s' % Engine_file)
    
    return sys.modules[__name__](template)
