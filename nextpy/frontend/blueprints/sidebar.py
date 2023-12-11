"""Builds a sidebar section for a webpage."""

import nextpy as xt


def sidebar(logo_src="/favicon.ico", title="Sidebar", menu_items=None, sidebar_style=None):
    """Create a customizable sidebar module.

    Args:
    - logo_src (str): Source path for the logo image.
    - title (str): Title for the sidebar.
    - menu_items (list): List of menu items. Each item should be a dict with 'label' and 'route'.
    - sidebar_style (dict): Custom style for the sidebar.

    Returns:
    - xt.Component: The sidebar component.
    """
    # Default sidebar style if none provided
    default_style = {
        "width": "250px",
        "padding_x": "2em",
        "padding_y": "1em",
        "background_color": "#333",
        "color": "white",
        "position": "fixed",
        "height": "100%",
        "left": "0px",
        "top": "0px",
        "z_index": "500"
    }
    combined_style = {**default_style, **(sidebar_style or {})}

    # Default menu items if none provided
    if menu_items is None:
        menu_items = [{"label": "Home", "route": "/"},
                      {"label": "About", "route": "/about"},
                      {"label": "Contact", "route": "/contact"}]

    # Create menu items
    menu = [
        xt.button(
            item['label'],
            color="white",
            background_color="transparent",
            border="none",
            padding="10px 20px",
            margin="5px 0"
        ) for item in menu_items
    ]

    # Sidebar layout
    return xt.box(
        xt.vstack(
            xt.image(src=logo_src, margin="0 auto"),
            xt.heading(title, text_align="center", margin_bottom="1em"),
            *menu,
        ),
        **combined_style
    )



