# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Welcome to Nextpy! This file outlines the steps to create a basic app."""
from xtconfig import config

import nextpy as xt

docs_url = "https://docs.dotagent.dev/nextpy/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class SliderVariation(xt.State):
    value: int = 50

    def set_end(self, value: int):
        self.value = value


def index() -> xt.Component:
    return xt.box(
        xt.animation(
                    xt.vstack(
                xt.heading(SliderVariation.value),
                xt.slider(on_change_end=SliderVariation.set_end),
                width="100vw",
            ),
            animate={"scale": [1, 2, 2, 1, 1],
                     "rotate": [0, 0, 180, 180, 0],
                     "borderRadius": ["0%", "0%", "50%", "50%", "0%"],
                    },
            transition={
                    "duration": 2,
                    "ease": "easeInOut",
                    "times": [0, 0.2, 0.5, 0.8, 1],
                    "repeat": "Infinity",
                    "repeatDelay": 1
                    },
            background_color="#fafafa"
        ),        
        class_name="flex justify-center items-center w-screen h-screen bg-[#7F00FF]"
    )


# Add state and page to the app.
app = xt.App()
app.add_page(index)