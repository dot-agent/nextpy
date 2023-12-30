# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import nextpy as xt
from nextpy_chat.templates import template
from nextpy_chat.components import sidebar
from nextpy_chat.components.interview import chat, navbar
from nextpy_chat import styles


@template(route='/interview_prep', title="InterviewPrep")
def interview_prep() -> xt.Component:
    """Inerview Preparation Page"""
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
