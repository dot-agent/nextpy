# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Builds a navbar section for a webpage."""
import nextpy as xt


def navbar(logo_src="favicon.ico", title="My App", menu_items=None):
    """Builds a navbar with logo, title, and menu items.
    
    Args:
        logo_src (str): Path to logo image file.
        title (str): Title text for navbar.
        menu_items (list): List of xt.menu_button items.
    

    Returns:
        nextpy.Element: The navbar component.
    """
    # Default menu items if none provided
    if menu_items is None:
        menu_items = [xt.menu_button("Menu")]

    return xt.box(
        xt.hstack(
            xt.image(src=logo_src),
            xt.heading(title),
        ),
        xt.spacer(),
        xt.menu(*menu_items),  # Unpack the list of menu items here
        position="fixed",
        width="100%",
        top="0px",
        z_index="5",
    )
