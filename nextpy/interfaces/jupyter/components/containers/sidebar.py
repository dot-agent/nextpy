from typing import Callable, Dict, List, Tuple, cast
import reacton 
import reacton.ipyvuetify as v
from reacton.core import Element

import nextpy.interfaces.jupyter as widget

@widget.component
def sidebar(children=[]):

    # TODO: generalize this, this is also used in title
    level = 0
    rc = reacton.core.get_render_context()
    context = rc.context
    while context and context.parent:
        level += 1
        context = context.parent
    offset = 2**level
    sidebar_portal.use_portal_add(children, offset)

    return widget.div(style="display; none")


PortalElements = Dict[str, List[Tuple[int, Element]]]

def _set_sidebar_default(updater: Callable[[PortalElements], PortalElements]):
    pass

class ElementPortal:
    def __init__(self):
        self.context = widget.create_context(_set_sidebar_default)

    # TODO: can we generalize the use of 'portals' ? (i.e. transporting elements from one place to another)
    def use_portal(self) -> List[Element]:
        portal_elements, set_portal_elements = widget.use_state(cast(PortalElements, {}))
        self.context.provide(set_portal_elements)  # type: ignore

        portal_elements_flat: List[Tuple[int, Element]] = []
        for uuid, value in portal_elements.items():
            portal_elements_flat.extend(value)
        portal_elements_flat.sort(key=lambda x: x[0])
        return [e[1] for e in portal_elements_flat]

    def use_portal_add(self, children: List[Element], offset: int):
        key = widget.use_unique_key(prefix="portal-")
        set_portal_elements = widget.use_context(self.context)
        values: List[Tuple[int, Element]] = []
        for i, child in enumerate(children):
            values.append((offset + i, child))

        # updates we do when children/offset changes
        def add():
            # we use the update function method, to avoid stale data
            def update_dict(portal_elements):
                portal_elements_updated = portal_elements.copy()
                portal_elements_updated[key] = values
                return portal_elements_updated

            set_portal_elements(update_dict)

        widget.use_effect(add, [values])

        # cleanup we only need to do after component removal
        def add_cleanup():
            def cleanup():
                def without(portal_elements):
                    portal_elements_restored = portal_elements.copy()
                    portal_elements_restored.pop(key, None)
                    return portal_elements_restored

                set_portal_elements(without)

            return cleanup

        widget.use_effect(add_cleanup, [])


sidebar_portal = ElementPortal()