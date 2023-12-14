"""Welcome to Nextpy! This file outlines the steps to create a basic app."""
from xtconfig import config

import nextpy as xt

docs_url = "https://docs.dotagent.dev/nextpy/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


class State(xt.State):
    """The app state."""

    pass


def Hero():
    return xt.fragment(
        # xt.color_mode_button(xt.color_mode_icon(), float="right"),
        xt.box(
            xt.vstack(
                xt.text(
                    "Branding | Image making ",
                    font_family="Epilogue",
                    # font_size="15.594px",
                    font_weight="bold",
                    class_name="md:mb-8 mb-4 text-xs md:text-base",
                ),
                xt.text(
                    "Visual",
                    # font_size="42.819px",
                    font_family="Epilogue",
                    font_weight="bold",
                    line_height="1px",
                    class_name="md:text-5xl text-3xl",
                ),
                xt.text(
                    "Designer",
                    font_family="Epilogue",
                    # font_size="42.819px",
                    font_weight="bold",
                    class_name="md:text-5xl text-3xl",
                ),
                xt.text(
                    "This is a template Figma file, turned into",
                    font_size="12.705px",
                    font_family="Epilogue",
                    class_name="pt-2",
                ),
                xt.text(
                    "code using Anima.",
                    line_height="5px",
                    font_size="12.705px",
                    font_family="Epilogue",
                ),
                xt.text(
                    "Learn more at AnimaApp.com",
                    font_size="12.705px",
                    font_family="Epilogue",
                ),
                # xt.text("David" + "\n" + "Henderson.", font_size="36px", line_height="40px"),
                xt.button(
                    xt.center(
                        "Contact",
                        bg="#2D2D2D",
                        color="white",
                        width="60%",
                        py="12px",
                        border_radius=None,
                        class_name="mt-6",
                    ),
                    variant="unstyled",
                ),
                spacing="0.5em",
                align_items="left",
                font_size="2em",
            ),
            xt.box(
                xt.center(
                    xt.image(
                        src="/image.png",
                        width="50%",
                    ),
                    font_size="15.25px",
                    color="#E3E3E3",
                    class_name="mt-20 md:mt-0 lg:mt-0",
                ),
            ),
            class_name="flex flex-col md:flex-row items-center justify-center",
            margin_top="6rem",
        ),
    )


def Card():
    return xt.box(
        xt.vstack(
            xt.text(
                "Latest work",
                font_size="16px",
                font_family="Epilogue",
                class_name=" text-center mt-12 md:mt-20 font-bold",
            ),
            xt.box(
                xt.box(
                    xt.image(src="/book.jpg", width="159.477px", height="159.477"),
                    xt.text(
                        "Project title",
                        font_size="9.665px",
                        font_family="Epilogue",
                        class_name="py-2",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_size="8.215px",
                        font_family="Epilogue",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/abstract.jpg",
                        width="159.477px",
                        height="159.477",
                        object_fit="cover",
                    ),
                    xt.text(
                        "Project title",
                        font_size="9.665px",
                        font_family="Epilogue",
                        class_name="py-2",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_size="8.215px",
                        font_family="Epilogue",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/magzine.jpg",
                        width="159.477px",
                        height="159.477",
                        object_fit="cover",
                    ),
                    xt.text(
                        "Project title",
                        font_size="9.665px",
                        font_family="Epilogue",
                        class_name="py-2",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_size="8.215px",
                        font_family="Epilogue",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/isalah.jpg",
                        width="159.477px",
                        height="159.477",
                        object_fit="cover",
                    ),
                    xt.text(
                        "Project title",
                        font_size="9.665px",
                        font_family="Epilogue",
                        class_name="py-2",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_size="8.215px",
                        font_family="Epilogue",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/book2.jpg",
                        width="159.477px",
                        height="159.477",
                        object_fit="cover",
                    ),
                    xt.text(
                        "Project title",
                        font_size="9.665px",
                        font_family="Epilogue",
                        class_name="py-2",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_size="8.215px",
                        font_family="Epilogue",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/book3.jpg",
                        width="159.477px",
                        height="159.477",
                        object_fit="cover",
                    ),
                    xt.text(
                        "Project title",
                        font_size="9.665px",
                        font_family="Epilogue",
                        class_name="py-2",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_size="8.215px",
                        font_family="Epilogue",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/magzine.jpg",
                        width="159.477px",
                        height="159.477",
                        object_fit="cover",
                    ),
                    xt.text(
                        "Project title",
                        font_size="9.665px",
                        font_family="Epilogue",
                        class_name="py-2",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_size="8.215px",
                        font_family="Epilogue",
                    ),
                ),
                xt.box(
                    xt.image(
                        src="/abstract.jpg",
                        width="159.477px",
                        height="159.477",
                        object_fit="cover",
                    ),
                    xt.text(
                        "Project title",
                        font_size="9.665px",
                        font_family="Epilogue",
                        class_name="py-2",
                    ),
                    xt.text(
                        "UI, Art drection",
                        font_size="8.215px",
                        font_family="Epilogue",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 md:pt-4 pt-2 gap-4",
            ),
            class_name="flex justify-center mb-12",
        ),
    )


def index() -> xt.Component:
    return xt.fragment(
        Hero(),
        Card(),
    )


# Add state and page to the app.
app = xt.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Epilogue&family=Nova+Square&display=swap",
    ],
)
app.add_page(index)
app.compile()
