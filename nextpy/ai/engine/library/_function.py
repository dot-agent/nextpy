# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from ._role import role

async def function(hidden=False, _parser_context=None, **kwargs):
    ''' A chat role block for the 'function' role.

    This is just a shorthand for {{#role 'function'}}...{{/role}}.

    Parameters
    ----------
    hidden : bool
        Whether to include the assistant block in future LLM context. 
    '''
    return await role(role_name="function", hidden=hidden, _parser_context=_parser_context, **kwargs)
function.is_block = True