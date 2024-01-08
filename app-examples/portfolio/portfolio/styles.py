import nextpy as xt


base_style = {
    xt.Text: {
        "font_family": "Epilogue",
    },
    xt.Button: {
        "bg": "#2D2D2D",
        "color": "white",
        "width": "30%",
        "border_radius": None,
        "_hover": {
            "bg": "#2D2D2D",
        },
    },
    xt.Input: {
        "_placeholder": {"color": "#2D2D2D"},
        "bg": "#F3F3F3",
        "border_radius": None,
        "height": "3rem",
    },
}
