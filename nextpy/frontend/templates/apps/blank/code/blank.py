from xtconfig import config
import nextpy as xt


# Style dictionary 
style = {
    "heading": {
        "text_align": "center",
        "font_size": "28px",  # Fixed font size
        "line_height": "36px", 
        "font_family": "DM Sans",
        "max_width": "620px",  # Fixed maximum width
        "padding_top": "16px",
        "padding_bottom": "16px", 
    },
    "get_started_box": {
        "font_family": "Inter",
        "text_align": "center",
        "font_size": "14px",  # Fixed font size
        "color": "black",
        "background": "white",
        "padding_x": "48px",  
        "padding_y": "12px",  # Fixed vertical padding
        "border_radius": "lg",
    },
    "vertical_stack_style": {
        "background": "#04090B",
        "height": "100vh",  # Using viewport height unit for full height
        "padding_top": "20%",  # Percentage-based padding for dynamic vertical spacing
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
app.compile()
