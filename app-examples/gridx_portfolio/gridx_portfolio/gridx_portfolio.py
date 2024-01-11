# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Welcome to Nextpy! This file outlines the steps to create a basic app."""
from xtconfig import config

import nextpy as xt

filename = f"{config.app_name}/{config.app_name}.py"


class State(xt.State):
    """The app state."""

    pass


def Navbar():
    return xt.box(
        xt.hstack(
            xt.image(src="logo.svg", width="90px"),
            xt.desktop_only(
                xt.hstack(
                    xt.text("Home"),
                    xt.text("About"),
                    xt.text("Works"),
                    xt.text("Contact"),
                    class_name="hidden md:flex gap-6 md:items-center md:space-x-6 text-white text-sm font-semibold",
                    font_family="Inter",
                    spacing="1.5rem",
                ),
            ),
            xt.button(
                xt.center(
                    "Lets Talk",
                    bg="#323232",
                    py="12px",
                    px="2rem",
                    class_name="hover:bg-white text-white hover:text-[#323232] text-sm font-semibold transition ease-in-out rounded-2xl",
                ),
                variant="unstyled",
                color_scheme="none",
            ),
            # xt.mobile_and_tablet(
            #     xt.menu(
            #     xt.menu_button("Menu"),
            # ),
            # ),
            justify_content="space-between",
            align_items="center",
        ),
        class_name="bg-[#0F0F0F] py-6 px-4 lg:px-48",
        # position="fixed",
        width="100%",
        # top="0px",
        z_index="5",
    )


def ProfileCard():
    return xt.box(
        xt.flex(
            xt.image(
                src="me.png",
                class_name="w-full max-w-[220px] md:max-w-[120px] xl:max-w-[220px] mb-4 md:mb-0 rounded-tl-3xl rounded-br-3xl",
                background="linear-gradient(90deg, #3c58e3 -15%, #c2ebff 58%, #5ab5e2 97%)",
            ),
            xt.vstack(
                xt.box(
                    xt.text("A WEB DEVELOPER", color="#BCBCBC", font_size="14px"),
                ),
                xt.vstack(
                    xt.text(
                        "David" + "\n" + "Henderson.",
                        font_size="36px",
                        line_height="40px",
                        color="#FFFFFF",
                    ),
                    xt.box(
                        xt.text(
                            "I am a Web Designer based" + "\n" + "in san francisco.",
                            color="#BCBCBC",
                            font_size="14px",
                        ),
                    ),
                    spacing="1em",
                ),
                align_items="start",
            ),
            class_name="flex flex-col md:flex-row items-center gap-[2rem]",
            spacing="2em",
        ),
        xt.vstack(xt.image(src="icon.svg", width="45px"), align_items="end"),
        font_family="Inter",
        class_name="p-4 md:p-6 bg-gradient-to-r from-[#202020] via-[#191919] to-[#161616] rounded-3xl ",
    )


def strip_card():
    return xt.box(
        xt.text("LATEST WORK AND FEATURED", font_size="14px", class_name="text-[#BCBCBC]"),
        font_family="Inter",
        class_name="py-4 px-6 bg-gradient-to-r from-[#202020] via-[#191919] to-[#161616] rounded-3xl ",
    )


def card_with_image_and_title(image_src, title, description):
    return xt.box(
        xt.vstack(
            xt.image(
                src=image_src,
                class_name="w-full max-w-[220px]",
            ),
            xt.hstack(
                xt.box(
                    xt.text(description, color="#BCBCBC", font_size="12px"),
                    xt.text(title, font_size="20px"),
                ),
                xt.image(src="icon.svg", width="45px"),
                justify_content="space-between",
                align_items="center",
                width="100%",
            ),
            spacing="1em",
        ),
        font_family="Inter",
        class_name="p-4 md:p-6 bg-gradient-to-r from-[#202020] via-[#191919] to-[#161616] rounded-3xl ",
    )


def services_card():
    return xt.box(
        xt.vstack(
            xt.hstack(
                xt.image(
                    src="camera.png",
                    class_name="w-full max-w-[40px] h-[40px]",
                ),
                xt.image(
                    src="design-pencil.png",
                    class_name="w-full max-w-[40px] h-[40px]",
                ),
                xt.image(
                    src="color-filter.png",
                    class_name="w-full max-w-[40px] h-[40px]",
                ),
                xt.image(
                    src="dev-mode-phone.png",
                    class_name="w-full max-w-[40px] h-[40px]",
                ),
                p=["0.5rem", "0.5rem", "2rem", "2rem", "2rem"],
                width="100%",
                justify_content="space-between",
                align_items="center",
            ),
            xt.hstack(
                xt.box(
                    xt.text("SPECIALIZATION", color="#BCBCBC", font_size="12px"),
                    xt.text("Services Offering", font_size="20px", color="#FFFFFF"),
                ),
                xt.image(src="icon.svg", width="45px"),
                width="100%",
                justify_content="space-between",
                align_items="center",
            ),
            justify_content="space-between",
            height="100%",
            spacing="1em",
        ),
        font_family="Inter",
        class_name="p-4 md:p-6 bg-gradient-to-r from-[#202020] via-[#191919] to-[#161616] rounded-3xl h-full",
    )


def experience_card():
    return xt.box(
        xt.flex(
            xt.vstack(
                xt.text("07", font_size="36px", line_height="40px", color="#FFFFFF"),
                xt.text(
                    "YEARS" + "\n" + "EXPERIENCE",
                    color="#BCBCBC",
                    font_size="14px",
                ),
                text_align="center",
                class_name="w-full md:w-auto lg:w-40 bg-gradient-to-r from-[#212121] via-[#222222] to-[#242424] rounded-3xl py-10 px-8",
            ),
            xt.vstack(
                xt.text("+125", font_size="36px", line_height="40px", color="#FFFFFF"),
                xt.text(
                    "CLIENTS" + "\n" + "WORLDWIDE",
                    color="#BCBCBC",
                    font_size="14px",
                ),
                text_align="center",
                class_name="w-full md:w-auto lg:w-40 bg-gradient-to-r from-[#212121] via-[#222222] to-[#242424] rounded-3xl py-10 px-8",
            ),
            xt.vstack(
                xt.text("+210", font_size="36px", line_height="40px", color="#FFFFFF"),
                xt.text(
                    "TOTAL" + "\n" + "PROJECTS",
                    color="#BCBCBC",
                    font_size="14px",
                ),
                text_align="center",
                class_name="w-full md:w-auto lg:w-40 bg-gradient-to-r from-[#212121] via-[#222222] to-[#242424] rounded-3xl py-10 px-8",
            ),
            class_name="flex h-full flex-row flex-wrap items-center justify-between gap-6 md:gap-0 lg:justify-center lg:gap-4",
            # wrap="wrap",
            # justify_content="space-between",
            # align_items="center",
            # spacing="1rem"
        ),
        font_family="Inter",
        class_name="p-4 md:p-6 bg-gradient-to-r from-[#202020] via-[#191919] to-[#161616] rounded-3xl gap-4 lg:p-3",
    )


def work_together_card():
    return xt.box(
        xt.box(
            xt.image(
                src="icon2.png",
                class_name="w-[37px] h-[76px] ml-6",
            ),
        ),
        xt.box(
            xt.vstack(
                xt.hstack(
                    xt.box(
                        xt.text("Let's", color="#FFFFFF"),
                        xt.span("work " , color="#FFFFFF"),
                        xt.span("together.", color="#5B78F6"),
                        line_height="52px",
                        font_size="44px",
                    ),
                    xt.image(src="icon.svg", width="45px"),
                    width="100%",
                    justify_content="space-between",
                    align_items="end",
                ),
                # spacing="1em",
                align_items="start",
            ),
            font_family="Inter",
            class_name="p-4 md:p-6",
        ),
        class_name="bg-gradient-to-r from-[#202020] via-[#191919] to-[#161616] rounded-3xl ",
    )


def index() -> xt.Component:
    return xt.fragment(
        Navbar(),
        xt.flex(
            xt.box(
                ProfileCard(),
                xt.box(
                    strip_card(),
                    xt.box(
                        card_with_image_and_title(
                            "sign.png", "Credentials", "MORE ABOUT ME"
                        ),
                        card_with_image_and_title(
                            "my-works.png", "Projects", "SHOWCASE"
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-6 text-white",
                    ),
                    class_name="grid grid-cols-1 gap-6",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
            ),
            xt.box(
                card_with_image_and_title("gfonts.png", "GFonts", "BLOG"),
                xt.box(
                    services_card(),
                    class_name="col-span-2",
                ),
                card_with_image_and_title("social.png", "Profiles", "STAY WITH ME"),
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
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap",  # This path is relative to assets/
    ],
)
app.add_page(index)

