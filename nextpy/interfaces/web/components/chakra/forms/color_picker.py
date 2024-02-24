from nextpy.interfaces.web.components.component import Component
# from nextpy import Var 
from typing import Any

class ColorPicker(Component):
    library = "react-colorful"
    tag = "HexColorPicker"
    color: str = None

    def get_event_triggers(self) -> dict[str, Any]:
        return {
            **super().get_event_triggers(),
            "on_change": lambda e0: [e0],
    }