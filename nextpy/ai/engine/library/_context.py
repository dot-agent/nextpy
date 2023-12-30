# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from ._role import role


async def context(hidden=False, _parser_context=None, **kwargs):
    """A chat role block for the 'context' role.

    This is just a shorthand for {{#role 'context'}}...{{/role}}.

    Parameters
    ----------
    hidden : bool
        Whether to include the assistant block in future LLM context.
    """
    return await role(
        role_name="context", hidden=hidden, _parser_context=_parser_context, **kwargs
    )


context.is_block = True