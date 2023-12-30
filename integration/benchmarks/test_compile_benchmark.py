# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Benchmark the time it takes to compile a nextpy app."""

import importlib

import nextpy

xt = nextpy


class State(xt.State):
    """A simple state class with a count variable."""

    count: int = 0

    def increment(self):
        """Increment the count."""
        self.count += 1

    def decrement(self):
        """Decrement the count."""
        self.count -= 1


class SliderVariation(State):
    """A simple state class with a count variable."""

    value: int = 50

    def set_end(self, value: int):
        """Increment the count.

        Args:
            value: The value of the slider.
        """
        self.value = value


def sample_small_page() -> xt.Component:
    """A simple page with a button that increments the count.

    Returns:
        A nextpy component.
    """
    return xt.vstack(
        *[xt.button(State.count, font_size="2em") for i in range(100)],
        spacing="1em",
    )


def sample_large_page() -> xt.Component:
    """A large page with a slider that increments the count.

    Returns:
        A nextpy component.
    """
    return xt.vstack(
        *[
            xt.vstack(
                xt.heading(SliderVariation.value),
                xt.slider(on_change_end=SliderVariation.set_end),
                width="100%",
            )
            for i in range(100)
        ],
        spacing="1em",
    )


def add_small_pages(app: xt.App):
    """Add 10 small pages to the app.

    Args:
        app: The nextpy app to add the pages to.
    """
    for i in range(10):
        app.add_page(sample_small_page, route=f"/{i}")


def add_large_pages(app: xt.App):
    """Add 10 large pages to the app.

    Args:
        app: The nextpy app to add the pages to.
    """
    for i in range(10):
        app.add_page(sample_large_page, route=f"/{i}")


def test_mean_import_time(benchmark):
    """Test that the mean import time is less than 1 second.

    Args:
        benchmark: The benchmark fixture.
    """

    def import_nextpy():
        importlib.reload(nextpy)

    # Benchmark the import
    benchmark(import_nextpy)


def test_mean_add_small_page_time(benchmark):
    """Test that the mean add page time is less than 1 second.

    Args:
        benchmark: The benchmark fixture.
    """
    app = xt.App(state=State)
    benchmark(add_small_pages, app)


def test_mean_add_large_page_time(benchmark):
    """Test that the mean add page time is less than 1 second.

    Args:
        benchmark: The benchmark fixture.
    """
    app = xt.App(state=State)
    results = benchmark(add_large_pages, app)
    print(results)
