# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Welcome to Nextpy! This file outlines the steps to create a basic app."""
import asyncio
import json

import httpx
from sqlmodel import select

import nextpy as xt

from .api import product_router
from .model import Product

DEFAULT_BODY = """{
    "code":"",
    "label":"",
    "image":"/favicon.ico",
    "quantity":0,
    "category":"",
    "seller":"",
    "sender":""
}"""

URL_OPTIONS = {
    "GET": "products",
    "POST": "products",
    "PUT": "products/{pr_id}",
    "DELETE": "products/{pr_id}",
}


class State(xt.State):
    """The app state."""

    products: list[Product]
    _db_updated: bool = False

    def load_product(self):
        with xt.session() as session:
            self.products = session.exec(select(Product)).all()
        yield State.reload_product

    @xt.background
    async def reload_product(self):
        while True:
            await asyncio.sleep(2)
            if self.db_updated:
                async with self:
                    with xt.session() as session:
                        self.products = session.exec(select(Product)).all()
                    self._db_updated = False

    @xt.var
    def db_updated(self):
        return self._db_updated

    @xt.var
    def total(self):
        return len(self.products)


class QueryState(State):
    body: str = DEFAULT_BODY
    response_code: str = ""
    response: str = ""
    method: str = "GET"
    url_query: str = URL_OPTIONS["GET"]
    query_options = list(URL_OPTIONS.keys())

    def update_method(self, value):
        if self.url_query == "":
            self.url_query = URL_OPTIONS[value]
        self.method = value

    @xt.var
    def need_body(self):
        return False

    @xt.var
    def f_response(self):
        return f"""```json\n{self.response}\n```"""

    def clear_query(self):
        self.url_query = URL_OPTIONS["GET"]
        self.method = "GET"
        self.body = DEFAULT_BODY

    async def send_query(self):
        url = f"http://localhost:8000/{self.url_query}"
        async with httpx.AsyncClient() as client:
            if self.method == "GET":
                res = await client.get(url)
            elif self.method == "POST":
                res = await client.post(url, data=self.body)
            elif self.method == "PUT":
                res = await client.put(url, data=self.body)
            elif self.method == "DELETE":
                res = await client.delete(url)
            else:
                res = None
        self.response_code = res.status_code
        if self.response_code == 200:
            self.response = json.dumps(res.json(), indent=2)
            self._db_updated = True
        else:
            self.response = res.content.decode()


def data_display():
    return xt.vstack(
        xt.text(State.total, " products found",),
        xt.foreach(State.products, render_product),
        xt.spacer(),
        justify_content="start",
        align_items="start",
        padding_x="1rem",
        # width="25%",
        height="100%",
        # bg="black"
    )


def render_product(product: Product):
    return xt.hstack(
        xt.image(src=product.image, height="100%", width="3vw"),
        xt.text(f"({product.code}) {product.label}", width="10vw"),
        xt.vstack(
            xt.text("Stock:", product.quantity),
            xt.text("Category:", product.category),
            spacing="0",
            # width="7vw",
        ),
        xt.vstack(
            xt.text("Seller:", product.seller),
            xt.text("Sender:", product.sender),
            spacing="0",
            # width="7vw",
        ),
        xt.spacer(),
        border="solid black 1px",
        width="100%",
    )


def query_form():
    return xt.vstack(
        xt.hstack(xt.heading("Simple CRUD")),
        xt.hstack(
            xt.text("Query:"),
            xt.select(
                ["GET", "POST", "PUT", "DELETE"],
                on_change=QueryState.update_method,
                variant="unstyled",
                background_color="transparent",
                border_style="solid",
                border_color="#23262f",
                p="0.75rem",
                border_width="2px",
                border_radius="0.5rem",
            ),
            xt.input(
                value=QueryState.url_query,
                on_change=QueryState.set_url_query,
                # width="30vw",
                variant="unstyled",
                background_color="transparent",
                border_style="solid",
                border_color="#23262f",
                p="0.75rem",
                border_width="2px",
                border_radius="0.5rem",
            ),
            width="100%",
        ),
        xt.vstack(
            xt.box(
                xt.text(
                    "Body:",
                    text_align="start",
                ),
                width="100%",
            ),
            xt.text_area(
                value=QueryState.body,
                height="30vh",
                on_change=QueryState.set_body,
                variant="unstyled",
                background_color="transparent",
                border_style="solid",
                border_color="#23262f",
                px="0.75rem",
                border_width="2px",
                border_radius="0.5rem",
            ),
            xt.hstack(
                xt.button(
                    "Clear",
                    on_click=QueryState.clear_query,
                    variant="unstyled",
                    py="0.5rem",
                    px="1.5rem",
                    border_radius="9999px",
                ),
                xt.button(
                    "Send",
                    on_click=QueryState.send_query,
                    variant="unstyled",
                    background_color="#3b71fe",
                    py="0.5rem",
                    px="1.5rem",
                    border_radius="9999px",
                ),
            ),
            width="100%",
            spacing="1rem",
        ),
        # xt.divider(orientation="horizontal", border="solid black 1px", width="100%"),
        xt.box(
            xt.hstack(
                xt.text("Status: ", QueryState.response_code), xt.spacer(), width="100%"
            ),
            xt.container(
                xt.markdown(
                    QueryState.f_response,
                    language="json",
                    height="30vh",
                ),
            ),
            width="100%",
        ),
        spacing="3rem",
        # width="50vw",
        width="100%",
    )


def index() -> xt.Component:
    return xt.flex(
        xt.spacer(),
        query_form(),
        xt.spacer(),
        xt.divider(orientation="vertical", border="solid black 1px"),
        xt.box(
            xt.heading("Data Display", font_size="24px", pb="1rem"),
            xt.divider(orientation="horizontal", border="solid #555555 1px"),
            data_display(),
            bg="black",
            border_radius="1rem",
            p="10px" 
        ),
        xt.spacer(),
        flex_direction=["column", "column", "row", "row", "row"],
        height="100%",
        width="100%",
        pt=["1rem", "1rem,", "1rem", "2rem", "2rem"],
        padding_x="1rem",
        gap="1rem",
        font_family="Poppins"
    )


# Add state and page to the app.
app = xt.App(
    style={
        "background_color": "#141718",
    },
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap",
    ],
)
app.add_page(index, on_load=State.load_product)

app.api.include_router(product_router)


