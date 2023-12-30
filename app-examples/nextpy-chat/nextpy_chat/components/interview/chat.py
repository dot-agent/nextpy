# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import nextpy as xt
from nextpy_chat import styles
from nextpy_chat.components import loading_icon
from nextpy_chat.State.interview import QA, InterviewState

def message(qa: QA) -> xt.Component:
    return xt.box(
        xt.box(
            xt.hstack(
                xt.image(
                    src='/avatar_smile.png', width='25px', height='25px'
                ),
                xt.text(
                    qa.question,
                    color = "white",
                    font_size = '12px',
                    shadow=styles.shadow_light,
                    py='4'
                ),
            ),
            text_align="left",
            bg = styles.bg_dark_color,
            p = '4',
            my = '2 em',
            width = "100%",
            class_name = "rounded-lg"
        ),
        xt.box(
            xt.image(
                src='/avatar.png', width='25px', height='25px'
            ),
            xt.text(
                qa.answer,
                shadow=styles.shadow_light,
                font_size = '12px',
                **styles.message_style,
            ),
            class_name="flex flex-row items-center",
            text_align="left"
        ),
        p = '1em',
        width="100%",
    )


def chat() -> xt.Component:
    """List all the messages in a single conversation."""
    return xt.vstack(
        xt.vstack(
        xt.card(
            xt.hstack(
                xt.image( src = "/logo.png", height = "30px", width = "30px", padding_right='3px' ),
                xt.text("Add JOB DESCRIPTION or JOB KEYWORD below and press Submit to start with INTERVIEW", font_size="xs", font_weight="bold")
            ),
            bg = '#00ADB5',
            color = "black",
            width = "40%",
        ),
        xt.form(
            xt.text_area(
                value = InterviewState.job_desc,
                is_required= True,
                placeholder = 'Enter Job Description',
                on_change=InterviewState.set_job_desc,
            ),
            xt.form_control(
                xt.button(
                    xt.text('SUBMIT'),
                    bg = '#00ADB5',
                    color = "black",
                    class_name = 'w-max',
                    type_ = 'submit',
                    my = '1em'
                ),
            ),
            on_submit=InterviewState.process_interview
        ),
        m = '6em',
        display = InterviewState.interview_option
        ),
        xt.box(
            xt.foreach(InterviewState.interview_chats[InterviewState.interview_chat], message)
        ),
        m = '1em',
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
                            value=InterviewState.interview_answer,
                            on_change=InterviewState.set_interview_answer,
                            _placeholder={"color": "#fffa"},
                            border_width="0px"
                        ),
                        xt.button(
                            xt.cond(
                                InterviewState.recording,
                                xt.image(src="/listen.png", width="2em", height="auto"),
                                xt.image(src="/mike.png", width="2em", height="auto"),
                            ),
                            on_click=InterviewState.start_recording,
                            bg=styles.accent_dark,
                            border_width="0px",
                        ),                
                        xt.button(
                            xt.cond(
                                InterviewState.interview_processing,
                                loading_icon(height="1em"),
                                xt.image(src="/send.svg", width="1.5em", height="auto"),
                            ),
                            type_="submit",
                            bg=styles.accent_dark,
                            border_width="0px",
                            rounded = "3xl"
                        )
                    ),
                    is_disabled=InterviewState.interview_processing,
                    style=styles.action_bar_style,
                    mx='auto'
                ),
                on_submit=InterviewState.process_interview,
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
        width = "100%",
        display = InterviewState.interview_convo
    )