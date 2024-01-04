import nextpy as xt


def contact():
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