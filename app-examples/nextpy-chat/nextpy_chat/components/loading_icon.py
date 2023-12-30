# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import nextpy as xt

class LoadingIcon(xt.Component):
    """A custom loading icon component."""

    library = "react-loading-icons"
    tag = "SpinningCircles"
    stroke: xt.Var[str]
    stroke_opacity: xt.Var[str]
    fill: xt.Var[str]
    fill_opacity: xt.Var[str]
    stroke_width: xt.Var[str]
    speed: xt.Var[str]
    height: xt.Var[str]

    def get_event_triggers(self) -> dict:
        return {"on_change": lambda status: [status]}


loading_icon = LoadingIcon.create