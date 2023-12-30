# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from nextpy.backend.event import EventChain
from nextpy.backend.vars import BaseVar
from nextpy.frontend.components.chakra.forms.form import Form


def test_render_on_submit():
    """Test that on_submit event chain is rendered as a separate function."""
    submit_it = BaseVar(
        _var_name="submit_it",
        _var_type=EventChain,
    )
    f = Form.create(on_submit=submit_it)
    exp_submit_name = f"handleSubmit_{f.handle_submit_unique_name}"  # type: ignore
    assert f"onSubmit={{{exp_submit_name}}}" in f.render()["props"]


def test_render_no_on_submit():
    """A form without on_submit should not render a submit handler."""
    f = Form.create()
    for prop in f.render()["props"]:
        assert "onSubmit" not in prop
