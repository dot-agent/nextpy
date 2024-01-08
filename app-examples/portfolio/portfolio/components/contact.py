import nextpy as xt


def contact():
    return xt.box(
        xt.box(
            xt.text(
                "Lets work together",
                class_name="md:mb-8 mb-4 font-bold text-base md:text-2xl lg:text-3xl",
            ),
            xt.text(
                "This is a template Figma file, turned into code using Anima. Learn more at AnimaApp.com This is a template Figma file, turned into code using Anima. Learn more at AnimaApp.com",
                class_name="md:mb-8 mb-4 text-sm lg:text-base max-w-lg",
            ),
            xt.box(
                xt.image(
                    src="/discord.svg",
                    class_name="w-7 h-7 object-cover md:w-9 md:h-9",
                ),
                xt.image(
                    src="/facebook.svg",
                    class_name="w-7 h-7 object-cover md:w-9 md:h-9",
                ),
                xt.image(
                    src="/dribbble.svg",
                    class_name="w-7 h-7 object-cover md:w-9 md:h-9",
                ),
                xt.image(
                    src="/instagram.svg",
                    class_name="w-7 h-7 object-cover md:w-9 md:h-9",
                ),
                xt.image(
                    src="/behance.svg",
                    class_name="w-7 h-7 object-cover md:w-9 md:h-9",
                ),
                class_name="flex items-center gap-4 ",
            ),
        ),
        xt.box(
            xt.input(
                placeholder="Name",
                class_name="mb-2",
            ),
            xt.input(
                placeholder="Email",
            ),
            xt.button(
                "Submit",
                class_name="mt-6 py-8 text-base md:text-lg",
            ),
            variant="unstyled",
            spacing="0.5em",
            align_items="left",
            font_size="2em",
        ),
        class_name="flex flex-col md:flex-row items-center justify-evenly gap-4 md:gap-8 mx-5  md:mx-8  pt-2 md:pt-12 lg:pt-14 pb-12 md:pb-20",
    )
