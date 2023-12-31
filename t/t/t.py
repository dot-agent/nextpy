from xtconfig import config

import nextpy as xt


def index() -> xt.Component:
    return xt.fragment(
        xt.hstack(
            xt.circular_progress(
                xt.circular_progress_label("⛽"),
                value=50,
            ),
            xt.circular_progress(
                xt.circular_progress_label("📶"),
                is_indeterminate=True,
            ),
        )
    )


# Add state and page to the app.
app = xt.App(
    # Add fonts here!
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,700&family=Inter&display=swap",
    ],
)
app.add_page(index)
