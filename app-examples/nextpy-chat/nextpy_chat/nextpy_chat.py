# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Welcome to Nextpy!."""

from nextpy_chat.pages import *
from nextpy_chat import styles
from nextpy_chat.State.state import State  
from nextpy_chat.components import chat, modal, navbar, sidebar
from nextpy_chat.templates import template

import nextpy as xt

@template(route='/', title="Index")
def index() -> xt.Component:
    """The main app."""
    return xt.vstack(
        navbar(),
        xt.vstack(
            chat.chat(),
            chat.action_bar(),
            width = "92%",
            align_self = "center",
            bg=styles.border_color,
            min_h="100vh",
            class_name = "rounded-md"
        ),
        sidebar(),
        bg=styles.bg_dark_color,
        color=styles.text_light_color,
        min_h="100vh",
        spacing="0",
    )



# Create the app and compile it.
app = xt.App(style=styles.base_style)


