from xtconfig import config

import nextpy as xt

# This code block represents a style dictionary generated using a large language model (LLM). 
# The original prompt for this generation was: "Generate a style dictionary for the following code [paste the code here]".
# Additionally, we have developed the "Nextpy Style Assistant", a tool designed to assist in code styling and best practices. 
# This assistant will be available on our Discord server soon for further support and guidance in code styling.

style = {
    "heading": {
        "text_align": "center",
        "font_size": "28px",
        "line_height": "36px",
        "color": "#F3F5F7",
        "font_family": "DM Sans",
        "max_width": "620px",
        "padding_top": "16px",
        "padding_bottom": "16px",
    },
    "get_started_box": {
        "font_family": "Inter",
        "text_align": "center",
        "font_size": "14px",
        "color": "black",
        "background": "white",
        "padding_x": "48px",
        "padding_y": "12px",
        "border_radius": "lg",
    },
    "vertical_stack_style": {
        "background": "#04090B",
        "height": "100vh",
        "padding_top": "20%",
        "padding_left":"5%",
        "padding_right":"5%",

    }
}

docs_url = "https://nextpy.org/nextpy/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"

class State(xt.State):
    """The app state."""

    pass

def index() -> xt.Component:
    return xt.fragment(
        xt.vstack(
            xt.image(src="/logo_darkmode.svg", width="150px"),
            xt.text("High performance web apps in pure python with built in AI functions", **style["heading"]),
            xt.box(
                "Get started by editing ",
                xt.span(filename, as_="b"), # `as_` exports it as <b> tag : Bold . Default is <p> tag . More at docs.nextpy.org/typography/text/
                xt.image(src="/gradient_underline.svg", width="150px"),
                **style["get_started_box"]
            ),
            **style["vertical_stack_style"]
        ),
    )

# Add state and page to the app.
app = xt.App(
    # Add fonts here!
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,700&family=Inter&display=swap",
    ],
)
app.add_page(index)
