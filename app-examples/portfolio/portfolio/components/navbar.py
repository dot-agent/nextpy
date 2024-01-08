import nextpy as xt

def navbar():
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