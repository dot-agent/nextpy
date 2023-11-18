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

# the user needs to set an LLM before they can use Compiler
llm = None

# This makes the Compiler module callable
class Compiler(types.ModuleType):
    def __call__(self, template, llm=None, cache_seed=0, logprobs=None, silent=None, async_mode=False, stream=None, caching=None, await_missing=False, logging=False, memory=None, memory_threshold=1, **kwargs):
        return Program(template, llm=llm, cache_seed=cache_seed, logprobs=logprobs, silent=silent, async_mode=async_mode, stream=stream, caching=caching, await_missing=await_missing, logging=logging, memory=memory, memory_threshold=memory_threshold, **kwargs)
sys.modules[__name__].__class__ = Compiler


def load(Compiler_file):
    ''' Load a Compiler program from the given text file.

    If the passed file is a valid local file it will be loaded directly.
    Otherwise, if it starts with "http://" or "https://" it will be loaded
    from the web.
    '''

    if os.path.exists(Compiler_file):
        with open(Compiler_file, 'r') as f:
            template = f.read()
    elif Compiler_file.startswith('http://') or Compiler_file.startswith('https://'):
        template = requests.get(Compiler_file).text
    else:
        raise ValueError('Invalid Compiler file: %s' % Compiler_file)
    
    return sys.modules[__name__](template)
