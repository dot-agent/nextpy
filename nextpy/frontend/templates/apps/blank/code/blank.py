# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import nextpy as xt

# Construct the filename to display 
from xtconfig import config
filename = f"{config.app_name}/{config.app_name}.py"

# define index page. Frontend Pages are just functions that return a frontend components
def index() -> xt.Component:
    return xt.fragment(
        xt.vstack(
            xt.image(src="/logo_darkmode.svg", width="150px"),
            xt.text(
                "High performance web apps in pure python with built in AI functions", 
                color="#F3F5F7",  # Hexadecimal color code for text
                font_size="28px",
                padding="12px",  # Space between an element and its border
                max_width="620px",  # Maximum width of the text element
            ),
            xt.box(
                "Get started by editing ",
                xt.span(filename, as_="b"),  # Bold text using <b> tag, default is <p> tag
                xt.image(src="/gradient_underline.svg", width="150px"),
                background="white",
                padding="12px 42px",  #  Vertical padding = 12px & Horizonal padding = 42px
                border_radius="lg",  # Large border radius
            ),
            height="100vh",  # Full viewport height
            background="#04090B",  # Background color
            padding_top="20%",  # Top padding percentage for responsive design
        ),
    )

# Global styles defined as a Python dictionary
style = {
    "text_align": "center",  
}


app = xt.App(style=style)
app.add_page(index)
