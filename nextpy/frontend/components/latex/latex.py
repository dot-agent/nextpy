from nextpy.frontend.components.component import Component
from nextpy.backend.vars import Var


class LatexWrapper(Component):
    """Component for rendering LaTeX in nextpy apps."""

    library = "react-latex-next"
    tag = "Latex"
    is_default = True
    
    # Define the props
    content: Var[str] = ""  # LaTeX content
    delimiters: Var[list] = [
        {"left": "$$", "right": "$$", "display": True},
        {"left": "\\(", "right": "\\)", "display": False},
    ]
    strict: Var[bool] = False
    macros: Var[dict] = {}
