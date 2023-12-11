import nextpy as xt

def navbar(logo_src="favicon.ico", title="My App", menu_items=None):
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