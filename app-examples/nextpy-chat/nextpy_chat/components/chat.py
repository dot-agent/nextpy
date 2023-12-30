# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import nextpy as xt
from nextpy_chat import styles
from nextpy_chat.components import loading_icon
from nextpy_chat.State.main import QA, MainState


def message(qa: QA) -> xt.Component:
    """A single question/answer message.

    Args:
        qa: The question/answer pair.

    Returns:
        A component displaying the question/answer pair.
    """

    return xt.box(
        xt.box(
            xt.image(
                src='/avatar.png', width='25px', height='25px'
            ),
            xt.text(
                qa.question,
                shadow=styles.shadow_light,
                font_size = '12px',
                **styles.message_style,
            ),
            class_name="flex flex-row items-center",
            text_align="left"
        ),
        xt.box(
            xt.hstack(
                xt.image(
                    src='/avatar_smile.png', width='25px', height='25px'
                ),
                xt.vstack(
                    xt.markdown(
                        qa.answer,
                        color = "white",
                        font_size = '12px',
                        shadow=styles.shadow_light
                    ),
                    class_name = 'p-6 text-xs'
                ),
            ),
            xt.hstack(
                xt.button(
                    xt.image( src='/like.png'),
                    on_click=MainState.toggle_like(qa.index),
                    style = styles.react_button,
                    bg = qa.like_bg               
                ),
                xt.button(
                    xt.image( src='/dislike.png'),
                    on_click=MainState.toggle_dislike(qa.index),
                    style = styles.react_button,
                    padding = '0.5',
                    bg = qa.dislike_bg
                ),
                px='9'
            ),
            text_align="left",
            bg = styles.bg_dark_color,
            p = '4',
            width = "100%",
            class_name = "rounded-lg"
        ),
        width="100%",
    )


def chat() -> xt.Component:
    """List all the messages in a single conversation."""
    return xt.vstack(
        xt.card(
            xt.hstack(
                xt.image( src = "/logo.png", height = "30px", width = "30px", padding_right='4px' ),
               xt.text("Hello! Welcome to NextpyGPT", font_size="sm", font_weight="bold")
            ),
            bg = '#00ADB5',
            color = "black",
            m = '1em',
            width = "30%",
            display = MainState.display_val,
        ),
        xt.box(
            xt.foreach(MainState.chats[MainState.current_chat], message),
        ),
        align_self="center",
        bg=styles.border_color,
        flex="1",
        mx='auto',
        overflow_y="hidden",
        width="90%",
        class_name="max-w-full md:max-w-[92%] h-screen scroll-smooth scrollbar-none scroll-auto"   
    )


def action_bar() -> xt.Component:
    """The action bar to send a new message."""
    return xt.box(
        xt.vstack(
            xt.form(
                xt.form_control(
                    xt.hstack(
                        xt.input(
                            placeholder="Type something...",
                            value=MainState.question,
                            on_change=MainState.set_question,
                            _placeholder={"color": "#fffa"},
                            border_width="0px"
                        ),
                        xt.button(
                            xt.cond(
                                MainState.processing,
                                loading_icon(height="1em"),
                                xt.image(src="send.svg", width="1.5em", height="auto"),
                            ),
                            type_="submit",
                            bg=styles.accent_dark,
                            border_width="0px",
                            rounded = "3xl"
                        )
                    ),
                    is_disabled=MainState.processing,
                    style=styles.action_bar_style,
                    mx='auto'
                ),
                on_submit=MainState.process_question,
            ),
            max_w="6xl",
            width="90%",
            mx="auto", 
        ),
        bg=styles.border_color,
        position="sticky",
        bottom="0",
        left="0",
        py="6",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top=f"1px solid {styles.border_color}",
        align_items = "center",
        width = "100%"
    )