"""Welcome to Nextpy! This file outlines the steps to create a basic app."""
from xtconfig import config

import nextpy as xt
from portfolio.components.navbar import navbar
from portfolio.components.hero import hero
from portfolio.components.contact import contact
from portfolio import styles

docs_url = "https://docs.dotagent.dev/nextpy/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(xt.State):
    """The app state."""

    pass


def Card():
    return xt.box(
        xt.vstack(
            xt.text(
                "Latest work",
                class_name="text-center text-xl md:text-3xl mt-16 md:mt-24 font-bold",
            ),
            xt.box(
                xt.box(
                    xt.image(
                        src="/book.jpg",
                        class_name="w-96 h-96 md:w-56 object-cover md:h-56 lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/abstract.jpg",
                        class_name="w-96 h-96 md:w-56 md:h-56 object-cover lg:w-80 lg:h-80 ",
                    ),
                    xt.text(
                        "Project title",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/magzine.jpg",
                        class_name="w-96 h-96 md:w-56 md:h-56 object-cover lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/isalah.jpg",
                        class_name="w-96 h-96 md:w-56 md:h-56 object-cover lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/book2.jpg",
                        class_name="w-96 h-96 md:w-56 md:h-56 object-cover lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/book3.jpg",
                        class_name="w-96 h-96 md:w-56 md:h-56 object-cover lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/magzine.jpg",
                        class_name="w-96 h-96 md:w-56 md:h-56 object-cover lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/abstract.jpg",
                        class_name="w-96 h-96 md:w-56 md:h-56 object-cover lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 md:pt-4 pt-2 px-4 md:px-2 gap-6",
            ),
            class_name="flex mb-8 md:mb-12 ",
        ),
    )


def index() -> xt.Component:
    return xt.fragment(
        navbar(),
        hero(),
        Card(),
        contact(),
    )


# Add state and page to the app.
app = xt.App(
    style=styles.base_style,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Epilogue&family=Nova+Square&display=swap",
    ],
)
app.add_page(index)
