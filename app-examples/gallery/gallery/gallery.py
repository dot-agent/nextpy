# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Welcome to Nextpy! This file outlines the steps to create a basic app."""
import csv
import nextpy as xt
from gallery import styles
from .templates import template

image_urls: list[str] = []
image_urls_csv = "assets/image_urls.csv"
with open(image_urls_csv, "r", newline="\n") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if len(row) > 0:
            url = row[0].strip()
            image_urls.append(url)


border_radius = ("0.375rem",)
box_shadow = ("0px 0px 0px 1px rgba(84, 82, 95, 0.14)",)
border = "1px solid #F4F3F6"
text_color = "black"
accent_text_color = "#1A1060"
accent_color = "#F5EFFE"


def add_item(category):
    return xt.vstack(
        xt.link(
            xt.image(
                src=category,
                height="100%",
                width="100%",
                fit="cover",
            ),
            height=["92vw", "15em", "15em", "15em", "15em"],
            width=["92vw", "15em", "15em", "15em", "15em"],
            href=f"{category}",
        ),
        box_shadow="lg",
        bg_color="white",
        _hover={
            "box_shadow": "rgba(38, 57, 77, .3) 0px 20px 30px -10px",
        },
        class_name = 'm-auto'
    )


def component_grid():
    return xt.box(
        xt.responsive_grid(
            xt.foreach(image_urls, add_item),
            columns=[1, 2, 3, 4, 5],
            gap=2,
        ),
    )


def gallery_with_no_sidebar():
    return xt.box(
        xt.vstack(
            component_grid(),
            align_items="stretch",
            min_height="80vh",
            margin_bottom="2em",
            overflow="hidden",
        ),
        class_name="w-max",
        flex_direction="column",
        overflow="hidden",
        position="relative",
    )


@template(route="/", title="GALLERY")
def gallery() -> xt.Component:
    return xt.vstack(
        xt.vstack(
            xt.vstack(
                xt.image(src="/logo.svg", width="170px"),
                xt.box(
                    "Browse our growing library of images. ",
                    text_align="center",
                    font_size=["14px", "16px", "18px", "24px", "28px"],
                    font_family="DM Sans",
                    color = 'white'
                ),
                bg="#04090B",
            ),
            xt.divider(),
            align_items="center",
        ),
        xt.hstack(
            xt.spacer(),
            gallery_with_no_sidebar(),
            xt.spacer(),
            align_items="flex-start",
            overflow="hidden",
        ),
        margin_top="2em",
        height="100%",
        position="relative",
        overflow_x="hidden",
    )


# Add state and page to the app.
app = xt.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,700&family=Inter&display=swap",]
)

