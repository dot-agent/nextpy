import nextpy as xt

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


def index():
    return xt.hstack(
        xt.button(
            "Decrement",
            bg="#fef2f2",
            color="#b91c1c",
            border_radius="lg",
            on_click=State.decrement,
        ),
        xt.heading(State.count, font_size="2em"),
        xt.text(State.message),
        xt.button(
            "Increment",
            bg="#ecfdf5",
            color="#047857",
            border_radius="lg",
            on_click=State.increment,
        ),
        spacing="1em",
    )

app = xt.App()
app.add_page(index)
