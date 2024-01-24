import nextpy as xt


def hero():
    return xt.fragment(
        # xt.color_mode_button(xt.color_mode_icon(), float="right"),
        xt.box(
            xt.box(
                xt.text(
                    "Branding | Image making ",
                    class_name="md:mb-8 mb-4 font-bold text-base md:text-lg",
                ),
                xt.text(
                    "Visual Designer",
                    class_name="md:text-7xl font-bold text-3xl",
                ),
                xt.text(
                    "This is a template Figma file, turned into code using Anima. Learn more at AnimaApp.com",
                    class_name="pt-2 md:text-sm max-w-md text-xs",
                ),
                xt.button(
                    "Contact",
                    class_name="py-8 mt-6  text-base md:text-lg",
                ),
                variant="unstyled",
                spacing="0.5em",
                align_items="left",
                font_size="2em",
            ),
            xt.box(
                xt.image(
                    src="/image.png",
                    class_name="w-4/6",
                ),
                font_size="15.25px",
                color="#E3E3E3",
                class_name="flex justify-center items-center",
            ),
            class_name="flex flex-col md:flex-row  items-center justify-evenly mx-5  md:mx-8 mt-16  md:mt-24    ",
        ),
    )
