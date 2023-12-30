# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import nextpy as xt

from nextpy_chat import styles
from nextpy_chat.State.main import MainState
from nextpy_chat.components import features


def navbar():
    return xt.box(
        xt.hstack(
            xt.hstack(
                xt.icon(
                    tag="hamburger",
                    mr=4,
                    on_click=MainState.toggle_drawer,
                    cursor="pointer",
                    w="1.2em",
                    h="1.2em",
                ),
                xt.link(
                    xt.box(
                        xt.image(src="/favicon.ico", width="1.2em", height="auto"),
                        p="1",
                        border_radius="6",
                        bg="#F0F0F0",
                        mr="2",
                    ),
                    href="/",
                ),
                xt.breadcrumb(
                    xt.breadcrumb_item(
                        xt.text(MainState.current_chat, size="sm", font_weight="normal"),
                    ),
                ),
            ),
            xt.hstack(
                # xt.button(
                #     "+ New chat",
                #     bg=styles.accent_color,
                #     px="4",
                #     py="2",
                #     h="auto",
                #     on_click=State.toggle_modal,
                # ),
                xt.hstack(
                        xt.image(src="/Frame.svg", width="1em", height="auto",class_name='min-w-[1em]',),
                        xt.input(
                                    placeholder="Ask the smartest AI agent",
                                    display=["none", "none", "none", "flex", "flex"],
                                    # value=MainState.question,
                                    # on_change=MainState.set_question,
                                    _placeholder={"color": "#6C7275", "font_size":"13px"},
                                    variant="unstyled",
                                    padding_right="8",
                                    padding_bottom="1"
                                ),
                    bg=styles.border_color,
                    rounded="xl",
                    padding_x="4",
                    padding_y="1",    
                ),
                features.features(),
                xt.menu(
                    xt.menu_button(
                        xt.avatar(name="User", size="sm"),
                        xt.box(),
                    ),
                    xt.menu_list(
                        xt.menu_item("Help"),
                        xt.menu_divider(),
                        xt.menu_item("Settings"),
                    ),
                ),
                spacing="6",
            ),
            justify="space-between",
        ),
        bg=styles.bg_dark_color,
        backdrop_filter="auto",
        backdrop_blur="lg",
        p="2",
        # border_bottom=f"1px solid {styles.border_color}",
        position="sticky",
        top="0",
        z_index="100",
    )