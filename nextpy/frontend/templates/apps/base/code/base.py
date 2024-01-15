# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Welcome to Nextpy!."""

from code import styles

# Import all the pages.
from code.pages import *

import nextpy as xt

class State(xt.State):
    """Define empty state to allow access to rx.State.router."""


# Create the app.
app = xt.App(style=styles.base_style)
