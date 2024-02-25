from typing import Dict, List, Optional, Union

import reacton.ipyvuetify as v

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter.util import _combine_classes


@widget.component
def card(
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    elevation: int = 2,
    margin=2,
    children: List[widget.Element] = [],
    classes: List[str] = [],
    style: Union[str, Dict[str, str], None] = None,
):
    """A card combines a title, subtitle, content and actions into a single unit.


    ## Example
    ```widget
    import nextpy.interfaces.jupyter

    @widget.component
    def Page():
        with widget.Card(title="Card title", subtitle="Card subtitle"):
            widget.Markdown(
                "Lorem ipsum dolor sit amet consectetur adipisicing elit. "\\
                "Commodi, ratione debitis quis est labore voluptatibus! "\\
                "Eaque cupiditate minima, at placeat totam, magni doloremque "\\
                "veniam neque porro libero rerum unde voluptatem!"
            )
            with widget.CardActions():
                widget.button("Action 1", text=True)
                widget.button("Action 2", text=True)
    ```


    ## Arguments

     * `title`: Title of the card.
     * `subtitle`: Subtitle of the card.
     * `elevation`: Elevation of the card, gives the appearance of hovering above the page.
     * `margin`: Margin of the card.
     * `children`: Children are placed as the main content of the card.
     * `style`: CSS style to apply to the top level element.
    """
    class_ = _combine_classes([f"ma-{margin}", *classes])
    style_flat = widget.util._flatten_style(style)
    children_actions = []
    children_text = []
    for child in children:
        if isinstance(child, widget.Element) and child.component == widget.CardActions:
            children_actions.extend(child.kwargs.get("children", []))
        else:
            children_text.append(child)
    with v.Card(elevation=elevation, class_=class_, style_=style_flat) as main:
        if title:
            with v.CardTitle(
                children=[title],
            ):
                pass
        if subtitle:
            with v.CardSubtitle(
                children=[subtitle],
            ):
                pass
        with v.CardText(children=children_text):
            pass
        if children_actions:
            with v.CardActions(children=children_actions):
                pass
    return main


@widget.component
def CardActions(children: List[widget.Element] = []):
    """Container for actions in a card.

    See [Card](/api/card) for an example.

    # Arguments

     * `children`: Children are placed as the action area of the card.
    """
    widget.Error("You should not see this if you add a CardActions as a child component of a Card")
