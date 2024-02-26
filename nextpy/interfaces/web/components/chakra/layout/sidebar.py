import nextpy as xt



def SidebarItem(text, href, class_name="", **kwargs):
    return xt.link(
        xt.text(text),
        class_name=f"text-md text-left {class_name}",
        href=href,
        bg="transparent",
        _hover={"bg": "#0A4075"},
        border_radius="999px",
        width="100%",
        pl="14px",
        py="6px",
        **kwargs,
    )


def Sidebar(
    *children,
    top="0px",
    **kwargs,
):
    return xt.box(
        xt.vstack(
            *children,
            spacing="4px",
            width="100%",
            align_items="start",
            pl="4px",
            pt="1rem",
            height="100%",
        ),
        display=["none", "block", "block"],
        width="15em",
        top=top,
        height=f"calc(100dvh - {top})",
        position="sticky",
        class_name="pt-4 pl-4 overflow-y-auto ",
        **kwargs,
    )
