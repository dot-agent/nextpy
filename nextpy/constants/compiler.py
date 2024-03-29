# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Compiler variables."""
import enum
from enum import Enum
from types import SimpleNamespace

from nextpy.base import Base
from nextpy.constants import Dirs
from nextpy.interfaces.web.imports import ReactImportVar

# The prefix used to create setters for state vars.
SETTER_PREFIX = "set_"

# The file used to specify no compilation.
NOCOMPILE_FILE = ".web/nocompile"


class Ext(SimpleNamespace):
    """Extension used in Nextpy."""

    # The extension for JS files.
    JS = ".js"
    # The extension for python files.
    PY = ".py"
    # The extension for css files.
    CSS = ".css"
    # The extension for zip files.
    ZIP = ".zip"


class CompileVars(SimpleNamespace):
    """The variables used during compilation."""

    # The expected variable name where the xt.App is stored.
    APP = "app"
    # The expected variable name where the API object is stored for deployment.
    API = "api"
    # The name of the router variable.
    ROUTER = "router"
    # The name of the socket variable.
    SOCKET = "socket"
    # The name of the variable to hold API results.
    RESULT = "result"
    # The name of the final variable.
    FINAL = "final"
    # The name of the process variable.
    PROCESSING = "processing"
    # The name of the state variable.
    STATE = "state"
    # The name of the events variable.
    EVENTS = "events"
    # The name of the initial hydrate event.
    HYDRATE = "hydrate"
    # The name of the is_hydrated variable.
    IS_HYDRATED = "is_hydrated"
    # The name of the function to add events to the queue.
    ADD_EVENTS = "addEvents"
    # The name of the var storing any connection error.
    CONNECT_ERROR = "connectError"
    # The name of the function for converting a dict to an event.
    TO_EVENT = "Event"
    # The name of the internal on_load event.
    ON_LOAD_INTERNAL = "on_load_internal"


class PageNames(SimpleNamespace):
    """The name of basic pages deployed in NextJS."""

    # The name of the index page.
    INDEX_ROUTE = "index"
    # The name of the app root page.
    APP_ROOT = "_app"
    # The root stylesheet filename.
    STYLESHEET_ROOT = "styles"
    # The name of the document root page.
    DOCUMENT_ROOT = "_document"
    # The name of the theme page.
    THEME = "theme"
    # The module containing shared stateful components
    STATEFUL_COMPONENTS = "stateful_components"


class ComponentName(Enum):
    """Component names."""

    BACKEND = "Backend"
    FRONTEND = "Frontend"

    def zip(self):
        """Give the zip filename for the component.

        Returns:
            The lower-case filename with zip extension.
        """
        return self.value.lower() + Ext.ZIP


class Imports(SimpleNamespace):
    """Common sets of import vars."""

    EVENTS = {
        "react": {ReactImportVar(tag="useContext")},
        f"/{Dirs.CONTEXTS_PATH}": {ReactImportVar(tag="EventLoopContext")},
        f"/{Dirs.STATE_PATH}": {ReactImportVar(tag=CompileVars.TO_EVENT)},
    }


class Hooks(SimpleNamespace):
    """Common sets of hook declarations."""

    EVENTS = f"const [{CompileVars.ADD_EVENTS}, {CompileVars.CONNECT_ERROR}] = useContext(EventLoopContext);"


class MemoizationDisposition(enum.Enum):
    """The conditions under which a component should be memoized."""

    # If the component uses state or events, it should be memoized.
    STATEFUL = "stateful"
    ALWAYS = "always"
    NEVER = "never"


class MemoizationMode(Base):
    """The mode for memoizing a Component."""

    # The conditions under which the component should be memoized.
    disposition: MemoizationDisposition = MemoizationDisposition.STATEFUL

    # Whether children of this component should be memoized first.
    recursive: bool = True
