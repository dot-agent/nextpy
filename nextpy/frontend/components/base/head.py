# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""The head component."""

from nextpy.frontend.components.component import Component, MemoizationLeaf


class NextHeadLib(Component):
    """Header components."""

    library = "next/head"


class Head(NextHeadLib, MemoizationLeaf):
    """Head Component."""

    tag = "NextHead"

    is_default = True
