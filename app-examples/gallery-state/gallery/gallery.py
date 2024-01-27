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

class State(xt.State):
    count: int = 0
    message: str = ""

    def increment(self):
        self.count += 1
        if self.count == 10:
            self.message = "Count is 10!"

    def decrement(self):
        self.count -= 1
        if self.count < 10:
            self.message = ""


@template(route="/", title="GALLERY")
def gallery() -> xt.Component:
    return xt.vstack(
        xt.vstack(
            xt.text(State.message, font_size="2em", text_color="white"),
            xt.input(value=State.message, on_change=State.set_message),
            xt.divider(),
            align_items="center",
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

