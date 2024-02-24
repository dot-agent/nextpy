import ipyvuetify as v
from ipywidgets import Widget

def expander(label: str, expanded: bool = False):
    # Adding a border with the `style_` attribute
    expander_header_style = "border: 1px solid #E0E0E0;"  # Example: solid gray border
    expander_header = v.ExpansionPanelHeader(children=[label], style_=expander_header_style)
    expander_content = v.ExpansionPanelContent()
    
    expander_panel = v.ExpansionPanel(children=[expander_header, expander_content], v_model=expanded, class_='elevation-2')
    
    expansion_panels = v.ExpansionPanels(children=[expander_panel])
    return expansion_panels

def add_content_to_expander(expansion_panels, content: Widget):
    expansion_panels.children[0].children[1].children = [content]
