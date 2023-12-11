"""Animation."""
from nextpy.frontend.components.framer.motion import MotionDiv


def animation(*args, **kwargs):
    """Create an animation component by wrapping motion_div."""
    return MotionDiv.create(*args, **kwargs)
