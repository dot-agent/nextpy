# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""The home page of the app."""

from code import styles
from code.templates import template

import nextpy as xt


@template(route="/", title="Home", image="/github.svg")
def index() -> xt.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    with open("README.md", encoding="utf-8") as readme:
        content = readme.read()
    return xt.markdown(content, component_map=styles.markdown_style)
