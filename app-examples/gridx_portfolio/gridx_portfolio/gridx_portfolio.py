# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts.
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Welcome to Nextpy! This file outlines the steps to create a basic app."""

import nextpy as xt

from gridx_portfolio.components.navbar import Navbar
from gridx_portfolio.components.cards import (
    ProfileCard,
    card_with_image_and_title,
    experience_card,
    services_card,
    strip_card,
    work_together_card,
)

@xt.page(title="GridX Portfolio", description="A portfolio website built with Nextpy")
def index() -> xt.Component:
    return xt.fragment(
        Navbar(),
        # aligning cards inside flexbox
        xt.flex(
            xt.box(
                ProfileCard(),
                xt.box(
                    strip_card(),
                    xt.box(
                        card_with_image_and_title(
                            image_src="sign.png",
                            title="Credentials",
                            description="MORE ABOUT ME",
                        ),
                        card_with_image_and_title(
                            image_src="my-works.png",
                            title="Projects",
                            description="SHOWCASE",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-6 text-white",
                    ),
                    class_name="grid grid-cols-1 gap-6",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
            ),
            xt.box(
                card_with_image_and_title(
                    image_src="gfonts.png", title="GFonts", description="BLOG"
                ),
                xt.box(
                    services_card(),
                    class_name="col-span-2",
                ),
                card_with_image_and_title(
                    image_src="social.png", title="Profiles", description="STAY WITH ME"
                ),
                class_name="grid grid-cols-1 md:grid-cols-4 md:gap-x-6 gap-y-6 text-white",
            ),
            xt.box(
                experience_card(),
                work_together_card(),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
            ),
            class_name="bg-[#0F0F0F] py-20 px-4 xl:px-48 flex flex-col gap-6",
        ),
    )


# Add state and page to the app.
app = xt.App(
    style={
        "font-family": "Inter",
    },
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap",  # This path is relative to assets/
    ],
)
app.add_page(index)
