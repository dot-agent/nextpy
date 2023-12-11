"""Sidebar component for the app."""
import nextpy as xt

from nextpy_chat import styles
from nextpy_chat.State.main import MainState


def sidebar_chat(chat: str) -> xt.Component:
    """A sidebar chat item.

    Args:
        chat: The chat item.
    """
    return xt.hstack(
        xt.box(
            chat,
            on_click=lambda: MainState.set_chat(chat),
            style=styles.sidebar_style,
            color=styles.icon_color,
            flex="1",
        ),
        xt.box(
            xt.icon(
                tag="delete",
                style=styles.icon_style,
                on_click=MainState.delete_chat,
            ),
            style=styles.sidebar_style,
        ),
        color=styles.text_light_color,
        cursor="pointer",
    )


def sidebar() -> xt.Component:
    """The sidebar component."""
    return xt.drawer(
        xt.drawer_overlay(
            xt.drawer_content(
                xt.drawer_header(
                    xt.hstack(
                        xt.text("Chats"),
                        xt.icon(
                            tag="close",
                            on_click=MainState.toggle_drawer,
                            style=styles.icon_style,
                        ),
                    )
                ),
                xt.drawer_body(
                    xt.vstack(
                        xt.foreach(MainState.chat_titles, lambda chat: sidebar_chat(chat)),
                        align_items="stretch",
                    )
                ),
            ),
        ),
        placement="left",
        is_open=MainState.drawer_open
    )