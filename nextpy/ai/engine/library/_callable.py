# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import builtins

def callable(value, _parser_context=None):
    ''' Check if the given value is callable.
    '''
    variable_stack = _parser_context["variable_stack"]

    function_call = variable_stack["llm.extract_function_call"](value)
    if function_call is not None:
        return True

    return builtins.callable(value)