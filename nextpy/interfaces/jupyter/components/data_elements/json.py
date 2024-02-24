import json
import reacton.ipyvuetify as v
from typing import Optional, Union
import nextpy.interfaces.jupyter as widget
import nextpy.interfaces.jupyter as xtj


def json_display(body: Union[object, str], *, expanded: bool = True):
    """
    Display an object or string as a pretty-printed JSON string within a Jupyter environment.
    
    Parameters:
    - body (object or str): The object to print as JSON. If a string, it is assumed to contain serialized JSON.
    - expanded (bool): If True, the JSON is displayed expanded. Defaults to True.
    """
    
    if not isinstance(body, str):
        body = json.dumps(body, indent=2)
    
    
    display_code = xtj.code(children=[body], style="white-space: pre-wrap;")
    
    
    if not expanded:
        display_code = v.ExpansionPanels(children=[
            v.ExpansionPanel(children=[
                v.ExpansionPanelHeader(children=["JSON Data"]),
                v.ExpansionPanelContent(children=[display_code])
            ])
        ])
    
    
    return display_code
