# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

def break_():
    """Breaks out of the current loop.

    This is useful for breaking out of a geneach loop early, typically this is used
    inside an `{{#if ...}}...{{/if}}` block.
    """
    raise StopIteration()
