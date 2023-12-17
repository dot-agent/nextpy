"""Welcome to Nextpy! This file outlines the steps to create a basic app."""
from xtconfig import config

import nextpy as xt

docs_url = "https://docs.dotagent.dev/nextpy/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(xt.State):
    """The app state."""

    pass


def Header():
    return xt.box(
        xt.text(
            "Logo",
        ),
        xt.box(
            xt.text("About", cursor="pointer"),
            xt.text("Work", cursor="pointer"),
            xt.text("Contact", cursor="pointer"),
            class_name="flex items-center gap-5 ",
        ),
        class_name="flex items-center justify-between mt-5 mx-5 md:mx-10",
    )


def Hero():
    return xt.fragment(
        # xt.color_mode_button(xt.color_mode_icon(), float="right"),
        xt.box(
            xt.box(
                xt.text(
                    "Branding | Image making ",
                    font_family="Epilogue",
                    font_weight="bold",
                    class_name="md:mb-8 mb-4 text-base md:text-lg",
                ),
                xt.text(
                    "Visual Designer",
                    font_family="Epilogue",
                    font_weight="bold",
                    class_name="md:text-7xl text-3xl",
                ),
                xt.text(
                    "This is a template Figma file, turned into code using Anima. Learn more at AnimaApp.com",
                    font_family="Epilogue",
                    class_name="pt-2 md:text-sm max-w-md text-xs",
                ),
                xt.button(
                    "Contact",
                    bg="#2D2D2D",
                    color="white",
                    width="30%",
                    border_radius=None,
                    class_name=" py-8 mt-6 hover:bg-[#2D2D2D]  text-base md:text-lg",
                    _hover={
                        "bg": "#2D2D2D",
                    },
                ),
                variant="unstyled",
                spacing="0.5em",
                align_items="left",
                font_size="2em",
            ),
            xt.box(
                xt.image(
                    src="/image.png",
                    class_name="w-3/6 md:w-4/6",
                ),
                font_size="15.25px",
                color="#E3E3E3",
                class_name="flex justify-center items-center",
            ),
            class_name="flex flex-col md:flex-row  items-center justify-evenly mx-5  md:mx-8 mt-16  md:mt-24    ",
        ),
    )


def Card():
    return xt.box(
        xt.vstack(
            xt.text(
                "Latest work",
                font_family="Epilogue",
                class_name="text-center md:text-3xl mt-16 md:mt-24 font-bold",
            ),
            xt.box(
                xt.box(
                    xt.image(
                        src="/book.jpg",
                        class_name="w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        font_family="Epilogue",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_family="Epilogue",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/abstract.jpg",
                        object_fit="cover",
                        class_name="w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        font_family="Epilogue",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_family="Epilogue",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/magzine.jpg",
                        object_fit="cover",
                        class_name="w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        font_family="Epilogue",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_family="Epilogue",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/isalah.jpg",
                        object_fit="cover",
                        class_name="w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        font_family="Epilogue",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_family="Epilogue",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/book2.jpg",
                        object_fit="cover",
                        class_name="w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        font_family="Epilogue",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_family="Epilogue",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/book3.jpg",
                        object_fit="cover",
                        class_name="w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        font_family="Epilogue",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_family="Epilogue",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/magzine.jpg",
                        object_fit="cover",
                        class_name="w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        font_family="Epilogue",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_family="Epilogue",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/abstract.jpg",
                        object_fit="cover",
                        class_name="w-48 h-48 md:w-60 md:h-60  lg:w-80 lg:h-80",
                    ),
                    xt.text(
                        "Project title",
                        font_family="Epilogue",
                        class_name="py-2 lg:text-base text-sm font-bold",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_family="Epilogue",
                        class_name="text-xs md:text-sm",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 md:pt-4 pt-2  gap-6",
            ),
            class_name="flex mb-12 ",
        ),
    )


def Contact():
    return xt.box(
        xt.box(
            xt.text(
                "Lets work together",
                font_family="Epilogue",
                font_weight="bold",
                class_name="md:mb-8 mb-4 text-base md:text-2xl lg:text-3xl",
            ),
            xt.text(
                "This is a template Figma file, turned into code using Anima. Learn more at AnimaApp.com This is a template Figma file, turned into code using Anima. Learn more at AnimaApp.com",
                font_family="Epilogue",
                class_name="md:mb-8 mb-4 text-sm lg:text-base max-w-lg",
            ),
            xt.box(
                xt.image(
                    src="/discord.svg",
                    object_fit="cover",
                    class_name="w-7 h-7 md:w-9 md:h-9",
                ),
                xt.image(
                    src="/facebook.svg",
                    object_fit="cover",
                    class_name=" w-7 h-7 md:w-9 md:h-9",
                ),
                xt.image(
                    src="/dribbble.svg",
                    object_fit="cover",
                    class_name="w-7 h-7 md:w-9 md:h-9",
                ),
                xt.image(
                    src="/nstagram.svg",
                    object_fit="cover",
                    class_name="w-7 h-7 md:w-9 md:h-9",
                ),
                xt.image(
                    src="/behance.svg",
                    object_fit="cover",
                    class_name="w-7 h-7 md:w-9 md:h-9",
                ),
                class_name="flex  items-center gap-4 ",
            ),
        ),
        xt.box(
            xt.input(
                placeholder="Name",
                _placeholder={"color": "#2D2D2D"},
                bg="#F3F3F3",
                border_radius=None,
                height="3rem",
                class_name="mb-2",
            ),
            xt.input(
                placeholder="Email",
                _placeholder={"color": "#2D2D2D"},
                bg="#F3F3F3",
                border_radius=None,
                height="3rem",
            ),
            xt.button(
                "Submit",
                bg="#2D2D2D",
                color="white",
                width="30%",
                border_radius=None,
                class_name="mt-6 py-8 text-base md:text-lg",
                _hover={
                    "bg": "#2D2D2D",
                },
            ),
            variant="unstyled",
            spacing="0.5em",
            align_items="left",
            font_size="2em",
        ),
        class_name="flex flex-col md:flex-row items-center justify-evenly gap-4 md:gap-8 mx-5  md:mx-8  pt-2 md:pt-12 lg:pt-14 pb-12 md:pb-20",
    )


def index() -> xt.Component:
    return xt.fragment(
        Header(),
        Hero(),
        Card(),
        Contact(),
    )


# Add state and page to the app.
app = xt.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Epilogue&family=Nova+Square&display=swap",
    ],
)
app.add_page(index)
app.compile()
