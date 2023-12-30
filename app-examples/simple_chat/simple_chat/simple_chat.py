# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Welcome to Nextpy!."""

from simple_chat.pages import *
from  simple_chat import styles
from simple_chat.State.main import MainState  
from simple_chat.components import chat, navbar, sidebar
from simple_chat.templates import template

import nextpy as xt

@template(route='/', title="Index")
def index() -> xt.Component:
    """The main app."""
    return xt.center(
        xt.form(
            xt.vstack(
                xt.heading(
                    'WELCOME TO NEXTPY GPT',
                    class_name = 'm-auto'
                ),
                xt.spacer(),
                xt.text(
                    'Please set OPENAI API KEY in your local environment variable'
                ),
                # xt.input(
                #     value = MainState.openai_api_key,
                #     placeholder = "Enter you OPENAI_API_KEY here",
                #     on_change = MainState.set_openai_api_key,
                #     id = 'openai_api_key'
                # ),
                xt.spacer(),
                xt.text(
                    'Select OPENAI API MODEL'
                ),
                xt.select(
                    MainState.model_options,
                    placeholder="Select an example.",
                    on_change=MainState.set_openai_api_model,
                    color_schemes="twitter",
                    id = 'openai_api_model'
                ),
                xt.spacer(),
                xt.button(
                    'SUBMIT',
                    type_ = 'submit'
                ),
                class_name = 'm-auto w-[60vw] h-[60vh]',
            ),
            on_submit = MainState.handle_openai_details,
        ),
        class_name = 'h-[100vh] w-[100vw] bg-black'
    )

# Create the app and compile it.
app = xt.App(style=styles.base_style)


