# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Animation."""
from nextpy.frontend.components.framer.motion import MotionDiv


def animation(*args, **kwargs):
    """Create an animation component by wrapping motion_div."""
    return MotionDiv.create(*args, **kwargs)
