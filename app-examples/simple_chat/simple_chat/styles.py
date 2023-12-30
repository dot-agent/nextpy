# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import nextpy as xt
from simple_chat.State.state import State

accent_color = "#5535d4"
accent_dark = "#141718"
accent_light = "#6649D8"

bg_dark_color = "#111"
bg_medium_color = "#222"
border_color = "#222327"

icon_color = "#fff8"

shadow_light = "rgba(17, 12, 46, 0.15) 0px 48px 100px 0px;"
shadow = "rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;"

text_light_color = "#fff"

message_style = dict(
    display="inline-block", 
    p="3", 
    border_radius="xl",
    # max_w = "30em"
)

input_style = dict(
    bg=accent_dark,
    border_color="#BDC1C6",
    border_width="1px",
    p="6",
    rounded='3xl',
)

action_bar_style = dict(
    bg=accent_dark,
    border_color="#BDC1C6",
    rounded='3xl',
    border_width="1px",
    align_self = "center",
    _hover={"border_color": accent_color}
)

icon_style = dict(
    font_size="md",
    color=icon_color,
    _hover=dict(color=text_light_color),
    cursor="pointer",
    w="8",
)

sidebar_style = dict(
    border="double 1px transparent;",
    border_radius="10px;",
    background_image=f"linear-gradient({bg_dark_color}, {bg_dark_color}), radial-gradient(circle at top left, {accent_color},{accent_dark});",
    background_origin="border-box;",
    background_clip="padding-box, border-box;",
    p="2",
    _hover=dict(
        background_image=f"linear-gradient({bg_dark_color}, {bg_dark_color}), radial-gradient(circle at top left, {accent_color},{accent_light});",
    ),
)

react_button = dict(
    # bg = "white",
    class_name = 'rounded-sm',
    height = '20px',
    max_w = "20px",
    max_h = '20px',
    min_w = '20px',
    min_h = '20px',
    padding = '1',
    width = '20px'
)

base_style = {
    xt.Avatar: {
        "shadow": shadow,
        "color": text_light_color,
        "bg": border_color,
    },
    xt.Button: {
        "shadow": shadow,
        "color": text_light_color,
        "_hover": {
            "bg": accent_dark,
        },
    },
    xt.Menu: {
        "bg": bg_dark_color,
        "border": f"red",
    },
    xt.MenuList: {
        "bg": bg_dark_color,
        "border": f"1.5px solid {bg_medium_color}",
    },
    xt.MenuDivider: {
        "border": f"1px solid {bg_medium_color}",
    },
    xt.MenuItem: {
        "bg": bg_dark_color,
        "color": text_light_color,
    },
    xt.DrawerContent: {
        "bg": bg_dark_color,
        "color": text_light_color,
        "opacity": "0.9",
    },
    xt.Hstack: {
        "align_items": "center",
        "justify_content": "space-between",
    },
    xt.Vstack: {
        "align_items": "stretch",
        "justify_content": "space-between",
    },
}