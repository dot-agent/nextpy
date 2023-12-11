"""Builds a hero section for a webpage."""
import nextpy as xt


def hero_section(title, subtitle, cta_text, background_image=None, hero_style=None):
    """Create a hero section for a webpage.

    Args:
    - title (str): The main title of the hero section.
    - subtitle (str): The subtitle or additional text.
    - cta_text (str): Text for the call-to-action button.
    - cta_on_click (callable): Function to call when the CTA button is clicked.
    - background_image (str, optional): URL of the background image.
    - hero_style (dict, optional): Custom styles for the hero section.

    Returns:
    - xt.Component: The hero section component.
    """
    # Default style for the hero section
    default_style = {
        "text_align": "center",
        "padding": "4em 1em",
        "background_image": f"url({background_image})" if background_image else None,
        "background_size": "cover",
        "background_position": "center",
        "color": "white"
    }

    # Combine default style with custom style
    combined_style = {**default_style, **(hero_style or {})}

    return xt.box(
        xt.vstack(
            xt.heading(title, level=1, margin_bottom="0.5em"),
            xt.text(subtitle, margin_bottom="1em"),
            xt.button(cta_text),
        ),
        align_items="center",
        justify_content="center",
        height="100vh",  # Full viewport height
        **combined_style
    )

# Example usage of the hero section
# hero_section = hero_section(
#     title="Welcome to Our Site",
#     subtitle="Discover our services and products",
#     cta_text="Learn More",
#     cta_on_click=lambda: xt.navigate("/learn-more"),
#     background_image="path/to/your/image.jpg"
# )
