import reacton.ipyvuetify as v
from typing import List, Optional, Union
import nextpy.interfaces.jupyter as widget


@widget.component
def tabs(
    tab_items: List[dict],
    class_name: str = '',
    style: str = '',
    **kwargs,
):
    
    # Create Tabs and TabItems
    tabs = [v.Tab(children=[item['title']]) for item in tab_items]
    tab_contents = [v.TabItem(children=[item['content']]) for item in tab_items]
    
    # Create Tabs container with slider
    tabs_container = v.Tabs(
        children=[
            *tabs,
            v.TabsSlider(),
            *tab_contents,
        ],
        class_=class_name,
        style_=style,
        **kwargs,
    )
    
    return tabs_container
