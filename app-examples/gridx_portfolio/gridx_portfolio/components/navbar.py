import nextpy as xt

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
                    class_name="hidden md:flex gap-6 md:items-center md:space-x-6 text-white text-base ",
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
            justify_content="space-between",
            align_items="center",
        ),
        class_name="bg-[#0F0F0F] py-6 px-4 lg:px-48",
        width="100%",
        z_index="5",
    )