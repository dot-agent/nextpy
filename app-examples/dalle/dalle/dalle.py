# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import nextpy as xt
from openai import OpenAI

import nextpy as xt

client = OpenAI()


class State(xt.State):
    """The app state."""

    prompt = ""
    image_url = ""
    processing = False
    complete = False

    def get_image(self):
        """Get the image from the prompt."""
        if self.prompt == "":
            return xt.window_alert("Prompt cannot be empty")

        self.processing = True
        self.complete = False
        yield

        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=self.prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            self.image_url = response.data[0].url
            self.complete = True
        except OpenAI.BadRequestError as e:
            error_info = e.args[0] if e.args else "An error occurred"
            xt.window_alert(f"Failed to generate image: {error_info}")
        finally:
            self.processing = False

        yield


style = {
    "font_family": "DM Sans",
    "font_size": "5vw",
    "::selection": {
        "background_color": "#2a9d8f",
    },
 
    xt.Input: {
        "background_color": "transparent",
        "border_style": "solid",
        "border_color": "#23262f",
        "padding_x": "0.75rem",
        "border_width": "2px",
        "border_radius": "0.5rem",
    },
}


def index():
    return xt.vstack(
        xt.vstack(
            xt.image(src="/logo.svg", width="170px"),
            xt.input(
                placeholder="Enter a prompt",
                on_blur=State.set_prompt,
                width="100%",
                variant="unstyled",
                p="0.75rem",
            ),
            xt.button(
                "Generate Image",
                on_click=State.get_image,
                is_loading=State.processing,
                variant="unstyled",
                background_color="#3b71fe",
                py="0.5rem",
                px="1.5rem",
                border_radius="9999px",
            ),
            xt.cond(
                State.complete,
                xt.image(
                    src=State.image_url,
                    class_name="rounded shadow-lg",
                ),
            ),
            spacing="2rem",
            pt="2rem",
            padding_x=["2em", "2em", "2em", "3em", "4em"],
            width="40em",
            max_width=["100vw", "100vw", "100vw", "79vw", "79vw"],
        ),
        width="100%",
        height="100dvh",
        class_name="bg-black",
    )


app = xt.App(
    style=style,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,700&family=Inter&display=swap",
    ],
)
app.add_page(index, title="nextpy:DALL·E")

