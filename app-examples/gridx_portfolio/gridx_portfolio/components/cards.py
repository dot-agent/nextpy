import nextpy as xt


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
        class_name="p-4 md:p-6 bg-gradient-to-r from-[#202020] via-[#191919] to-[#161616] rounded-3xl ",
    )


def strip_card():
    return xt.box(
        xt.text(
            "LATEST WORK AND FEATURED", font_size="14px", class_name="text-[#BCBCBC]"
        ),
        class_name="py-4 px-6 bg-gradient-to-r from-[#202020] via-[#191919] to-[#161616] rounded-3xl ",
    )


def card_with_image_and_title(image_src, title, description):
    return xt.box(
        xt.vstack(
            xt.image(
                src=image_src,
                class_name="w-full max-w-[300px] md:max-w-[220px]",
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
            class_name="min-h-[280px] md:min-h-0 flex justify-between",
            spacing="1em",
        ),
        class_name="p-4 md:p-6 bg-gradient-to-r from-[#202020] via-[#191919] to-[#161616] rounded-3xl ",
    )


class ImageGalleryState(xt.State):
    image_paths = [
        "camera.png",
        "design-pencil.png",
        "color-filter.png",
        "dev-mode-phone.png",
    ]


def services_card():
    return xt.box(
        xt.vstack(
            xt.hstack(
                xt.foreach(
                    ImageGalleryState.image_paths,
                    lambda image_path: xt.image(
                        src=image_path,
                        class_name="w-full max-w-[40px] h-[40px]",
                    ),
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
        ),
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
                        xt.span("work ", color="#FFFFFF"),
                        xt.span("together.", color="#5B78F6"),
                        line_height="52px",
                        font_size="44px",
                    ),
                    xt.image(src="icon.svg", width="45px"),
                    width="100%",
                    justify_content="space-between",
                    align_items="end",
                ),
                align_items="start",
            ),
            class_name="p-4 md:p-6",
        ),
        class_name="bg-gradient-to-r from-[#202020] via-[#191919] to-[#161616] rounded-3xl flex flex-col justify-between ",
    )
