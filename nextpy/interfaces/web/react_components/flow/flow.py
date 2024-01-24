# Import necessary modules from Nextpy
from nextpy.interfaces.web.react_components.component import Component, NoSSRComponent
from typing import Any, Dict, List, Union
from nextpy.backend.vars import Var

# Define ReactFlowLib component as the base class
class ReactFlowLib(NoSSRComponent):
    """A component that wraps a react flow lib."""
    library = "reactflow"

    def _get_custom_code(self) -> str:
        return """import 'reactflow/dist/style.css';"""

# Define Background component
class Background(ReactFlowLib):
    tag = "Background"
    color: Var[str] = "#ddd"  # Default color
    gap: Var[int] = 16        # Default gap
    size: Var[int] = 1        # Default size
    variant: Var[str] = "dots"  # Default variant

# Define Controls component
class Controls(ReactFlowLib):
    tag = "Controls"

# Define ReactFlow component
class ReactFlow(ReactFlowLib):
    tag = "ReactFlow"
    nodes: Var[List[Dict[str, Any]]]
    edges: Var[List[Dict[str, Any]]]
    fit_view: Var[bool] = True
    nodes_draggable: Var[bool] = True
    nodes_connectable: Var[bool] = True
    nodes_focusable: Var[bool] = True

    def get_event_triggers(self) -> dict[str, Any]:
        return {
            "on_nodes_change": lambda e0: [e0],
            "on_edges_change": lambda e0: [e0],
            "on_connect": lambda e0: [e0],
        }

    # Include Background and Controls by default in create method
    @classmethod
    def create(cls, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]], on_connect, **kwargs):
        # Create the background and controls components with default values
        background = Background.create()
        controls = Controls.create()
        # Return the ReactFlow component with background and controls included
        return super().create(
            background,
            controls,
            nodes=nodes,
            edges=edges,
            on_connect=on_connect,
            **kwargs
        )

# MiniMap component  
class MiniMap(ReactFlowLib):  
    tag = "MiniMap"  
    # Additional MiniMap properties can be added here  
  
# Panel component  
class Panel(ReactFlowLib):  
    tag = "Panel"  
    position: Var[str]  # e.g., "top-left", "top-center", "top-right", etc.
