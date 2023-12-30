# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from ._if import if_

async def unless(value, _parser_context=None):
    return await if_(value, invert=True, _parser_context=_parser_context)
unless.is_block = True