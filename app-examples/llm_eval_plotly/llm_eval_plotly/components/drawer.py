# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import nextpy as xt
from llm_eval_plotly.data.data import llm_eval_result


class DrawerState(xt.State):
    show_left: bool = False
    display_arrow: str = "visible"
    table_data = llm_eval_result

    def left(self):
        self.show_left = not self.show_left
        if self.show_left == True:
            self.display_arrow = "none"
        else:
            self.display_arrow = "visible"


def drawer_sidebar() -> xt.Component:
    return xt.box(
        xt.button(
            xt.image(src="/arrow.png", height="15px", width="15px"),
            display=DrawerState.display_arrow,
            on_click=DrawerState.left,
            class_name="absolute top-2 left-2 border-2 border-black rounded-md",
        ),
        xt.drawer(
            xt.drawer_overlay(
                xt.drawer_content(
                    xt.drawer_header(
                        xt.button(
                            xt.image(src="/close.png", height="15px", width="15px"),
                            on_click=DrawerState.left,
                            class_name="",
                        ),
                        xt.heading("Eval Markdown Input"),
                    ),
                    xt.drawer_body(
                        xt.text("Paste your markdown text here (no triple quotes)"),
                        xt.text_area(
                            value=DrawerState.table_data,
                            on_change=DrawerState.set_table_data,
                            height="400px",
                            class_name="rounded-md",
                        ),
                    ),
                    bg="rgba(0, 0, 0, 0.3)",
                )
            ),
            placement="left",
            is_open=DrawerState.show_left,
            size="md",
        ),
        class_name="fixed left-0",
    )
