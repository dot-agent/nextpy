from __future__ import annotations

from typing import Any, Dict, Union, Literal

from nextpy.constants import EventTriggers
from nextpy.frontend.components.component import Component
from nextpy.backend.vars import Var


class FramerMotion(Component):
    """A component that wraps all the framer motion components."""

    library = "framer-motion"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = None
        self.is_default = False

    # Animation target values.
    animate: Var[Any]
    
    # Initial animation values.
    initial: Var[Any]

    # Function for manual control of the transform string.
    transformTemplate: Var[str]

    # Animation when component exits the React tree.
    exit: Var[Dict[str, Any]]

    # Controls animation transitions.
    transition: Var[Dict[str, Any]]

    # Named animation variants.
    variants: Var[Dict[Any, Any]]

    # Whether layout should animate.
    layout: Var[Union[bool, Literal["position", "size"]]]

    # Unique ID for shared layout animations.
    layoutId: Var[str]

    # Dependency values causing component re-layout.
    layoutDependency: Var[Any]

    # Scroll component into view on layout change.
    layoutScroll: Var[bool]

    # Inherit animations from parent.
    inherit: Var[bool]

    # Animation on hover.
    whileHover: Var[Dict[str, Any]]

    # Animation on tap or click.
    whileTap: Var[Dict[str, Any]]

    # Animation on focus.
    whileFocus: Var[Dict[str, Any]]

    # Enable drag and its direction (x, y, or both).
    drag: Var[Union[bool, Literal["x", "y"]]]

    # Animation during drag.
    whileDrag: Var[Any]

    # Animation when component is in view.
    whileInView: Var[Any]

    # Constraints for drag motion.
    dragConstraints: Var[Any]

    # Snap back to origin post drag.
    dragSnapToOrigin: Var[bool]

    # Elasticity of drag motion.
    dragElastic: Var[int]

    # Maintain momentum post drag.
    dragMomentum: Var[bool]

    # Transition of drag motion.
    dragTransition: Var[Dict[str, Any]]

    # Propagate drag motion through children.
    dragPropagation: Var[bool]

    # Reference to manual drag controls.
    dragControls: Var[Any]

    # Listen to drag events.
    dragListener: Var[bool]

    def get_event_triggers(self) -> dict[str, Union[Var, Any]]:
        """Get the event triggers that pass the component's value to the handler.

        Returns:
            A dict mapping the event trigger to the var that is passed to the handler.
        """
        return {
            EventTriggers.ON_CLICK: lambda: [],
            EventTriggers.ON_MOUSE_ENTER: lambda: [],
            EventTriggers.ON_MOUSE_MOVE: lambda: [],
            EventTriggers.ON_MOUSE_LEAVE: lambda: [],
        }

        

# The classes that inherits the FramerMotion class and each of these classes denote a html element used with "motion." suffix to use as a motion component
class MotionA(FramerMotion):
    """A framer motion component that wraps motion.a element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.a"


class MotionArticle(FramerMotion):
    """A framer motion component that wraps motion.Article element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.article"


class MotionAside(FramerMotion):
    """A framer motion component that wraps motion.aside element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.aside"


class MotionButton(FramerMotion):
    """A framer motion component that wraps motion.button element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.button"


class MotionDiv(FramerMotion):
    """A framer motion component that wraps motion.div element."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.div"


class MotionFieldset(FramerMotion):
    """A framer motion component that wraps motion.fieldset element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.fieldset"


class MotionFooter(FramerMotion):
    """A framer motion component that wraps motion.footer element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.footer"


class MotionForm(FramerMotion):
    """A framer motion component that wraps motion.form element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.form"


class MotionH1(FramerMotion):
    """A framer motion component that wraps motion.h1 element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.h1"


class MotionH2(FramerMotion):
    """A framer motion component that wraps motion.h2 element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.h2"


class MotionH3(FramerMotion):
    """A framer motion component that wraps motion.h3 element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.h3"


class MotionH4(FramerMotion):
    """A framer motion component that wraps motion.h4 element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.h4"


class MotionH5(FramerMotion):
    """A framer motion component that wraps motion.h5 element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.h5"


class MotionH6(FramerMotion):
    """A framer motion component that wraps motion.h6 element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.h6"


class MotionHeader(FramerMotion):
    """A framer motion component that wraps motion.header element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.header"


class MotionImg(FramerMotion):
    """A framer motion component that wraps motion.img element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.img"


class MotionInput(FramerMotion):
    """A framer motion component that wraps motion.input element."""

    tag = "motion.input"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.h6"

    @property
    def animate(self):
        return {"x": self.x, "y": self.y, "z": self.z}


class MotionLabel(FramerMotion):
    """A framer motion component that wraps motion.label element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.label"


class MotionLi(FramerMotion):
    """A framer motion component that wraps motion.li element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.li"


class MotionMain(FramerMotion):
    """A framer motion component that wraps motion.main element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.main"


class MotionNav(FramerMotion):
    """A framer motion component that wraps motion.nav element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.nav"


class MotionOl(FramerMotion):
    """A framer motion component that wraps motion.ol element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.ol"


class MotionOption(FramerMotion):
    """A framer motion component that wraps motion.option element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.option"


class MotionP(FramerMotion):
    """A framer motion component that wraps motion.p element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.p"


class MotionSection(FramerMotion):
    """A framer motion component that wraps motion.section element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.section"


class MotionSelect(FramerMotion):
    """A framer motion component that wraps motion.select element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.select"


class MotionSpan(FramerMotion):
    """A framer motion component that wraps motion.span element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.span"


class MotionTable(FramerMotion):
    """A framer motion component that wraps motion.table element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.table"


class MotionTd(FramerMotion):
    """A framer motion component that wraps motion.td element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.td"


class MotionTextArea(FramerMotion):
    """A framer motion component that wraps motion.textarea element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.textarea"


class MotionTh(FramerMotion):
    """A framer motion component that wraps motion.th element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.th"


class MotionTr(FramerMotion):
    """A framer motion component that wraps motion.tr element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.tr"


class MotionUl(FramerMotion):
    """A framer motion component that wraps motion.ul element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = "motion.ul"