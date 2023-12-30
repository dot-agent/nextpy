# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Styles for the app."""

import nextpy as xt

app_general_style = {
    "_dark": {
        "bg": "#15171b"
    }
}

animation_dots = {
    "@keyframes dots":{
        "0%": {"background_position": "0 0"},
        "100%": {"background_position": "40px 40px"}
    },
    "animation": "dots 4s linear infinite alternate-reverse both"
}

animation_wave = {
    "@keyframes wave":{
        "0%": {"transform": "rotate(25deg)"},
        "100%": {"transform": "rotate(-15deg)"}
    },
    "animation": "wave 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite alternate both"
}

main_style = {
    "property":{
        "width": "100%",
        "height": "84vh",
        "padding": "15rem 0rem",
        "align_items": "center",
        "justify_content": "start"
    }
}

header_style = {
    "width" : "100%",
    "height": "50px",
    "padding" : ["0rem" "1rem", "0rem", "1rem","0rem" "1rem", "0rem", "8rem","0rem" "8rem"],
    "transition" : "all 550ms ease",
}

footer_style = {
    "width" : ["100%", "90%", "60%", "45%" , "45%"],
    "height": "50px",
    "align_items": "center",
    "justify_content": "center"
}

border_radius = "0.375rem"
box_shadow = "0px 0px 0px 1px rgba(84, 82, 95, 0.14)"
border = "1px solid #F4F3F6"
text_color = "black"
accent_text_color = "#1A1060"
accent_color = "#F5EFFE"
hover_accent_color = {"_hover": {"color": accent_color}}
hover_accent_bg = {"_hover": {"bg": accent_color}}
content_width_vw = "90vw"
sidebar_width = "20em"

template_page_style = {"padding_top": "5em", "padding_x": ["auto", "2em"]}

template_content_style = {
    "width": "100%",
    "align_items": "flex-start",
    "box_shadow": box_shadow,
    "border_radius": border_radius,
    "padding": "1em",
    "margin_bottom": "2em",
}

link_style = {
    "color": text_color,
    "text_decoration": "none",
    **hover_accent_color,
}

overlapping_button_style = {
    "background_color": "white",
    "border": border,
    "border_radius": border_radius,
}

base_style = {
    xt.MenuButton: {
        "width": "3em",
        "height": "3em",
        **overlapping_button_style,
    },
    xt.MenuItem: hover_accent_bg,
}

markdown_style = {
    "code": lambda text: xt.code(text, color="#1F1944", bg="#EAE4FD"),
    "a": lambda text, **props: xt.link(
        text,
        **props,
        font_weight="bold",
        color="#03030B",
        text_decoration="underline",
        text_decoration_color="#AD9BF8",
        _hover={
            "color": "#AD9BF8",
            "text_decoration": "underline",
            "text_decoration_color": "#03030B",
        },
    ),
}
