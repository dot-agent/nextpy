import nextpy as xt


class CounterState(xt.State):
    value: int = 0
    
    def change_value(self, amount):
        self.value += amount


def create_button(label, amount):
    return xt.unstyled.button(
        label,
        on_click=lambda: CounterState.change_value(amount)
    )


def index() -> xt.Component:
    heading_color = xt.match(
        CounterState.value,
        (0, "red"),
        (4, "blue"),
        (8, "green"),
        (12, "orange"),
        (16, "lime"),
        (20, "orange"),
        "black"
    )

    return xt.unstyled.flex(
        xt.unstyled.heading(
            CounterState.value, 
            color="white",
            background_color=heading_color,
            as_="h2"
        ),
        xt.unstyled.flex(
            create_button("decrement", -1),
            create_button("increment", 1),
            gap="2"
        ),
        align_items="center",
        direction="column",
        gap="2"
    )


# Global styles defined as a Python dictionary
style = {
    "text_align": "center",  
}

app = xt.App(style=style)
app.add_page(index)
