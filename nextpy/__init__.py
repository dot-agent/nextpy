"""Import all classes and functions the end user will need to make an app.

Anything imported here will be available in the default nextpy import as `xt.*`.
To signal to typecheckers that something should be reexported,
we use the Flask "import name as name" syntax
"""
from __future__ import annotations

import importlib
from typing import Type

from nextpy.frontend.page import page as page
from nextpy.utils import console
from nextpy.utils.format import to_snake_case

_ALL_COMPONENTS = [
    "Accordion",
    "AccordionButton",
    "AccordionIcon",
    "AccordionItem",
    "AccordionPanel",
    "Alert",
    "AlertDescription",
    "AlertDialog",
    "AlertDialogBody",
    "AlertDialogContent",
    "AlertDialogFooter",
    "AlertDialogHeader",
    "AlertDialogOverlay",
    "AlertIcon",
    "AlertTitle",
    "AspectRatio",
    "Audio",
    "Avatar",
    "AvatarBadge",
    "AvatarGroup",
    "Badge",
    "Box",
    "Breadcrumb",
    "BreadcrumbItem",
    "BreadcrumbLink",
    "BreadcrumbSeparator",
    "Button",
    "ButtonGroup",
    "Card",
    "CardBody",
    "CardFooter",
    "CardHeader",
    "Center",
    "Checkbox",
    "CheckboxGroup",
    "CircularProgress",
    "CircularProgressLabel",
    "Circle",
    "Code",
    "CodeBlock",
    "Collapse",
    "ColorModeButton",
    "ColorModeIcon",
    "ColorModeSwitch",
    "Component",
    "Cond",
    "ConnectionBanner",
    "ConnectionModal",
    "Container",
    "DataTable",
    "DataEditor",
    "DataEditorTheme",
    "DatePicker",
    "DateTimePicker",
    "DebounceInput",
    "Divider",
    "Drawer",
    "DrawerBody",
    "DrawerCloseButton",
    "DrawerContent",
    "DrawerFooter",
    "DrawerHeader",
    "DrawerOverlay",
    "Editable",
    "EditableInput",
    "EditablePreview",
    "EditableTextarea",
    "Editor",
    "Email",
    "Fade",
    "Flex",
    "Foreach",
    "Form",
    "FormControl",
    "FormErrorMessage",
    "FormHelperText",
    "FormLabel",
    "Fragment",
    "Grid",
    "GridItem",
    "Heading",
    "Highlight",
    "Hstack",
    "Html",
    "Icon",
    "IconButton",
    "Image",
    "Input",
    "InputGroup",
    "InputLeftAddon",
    "InputLeftElement",
    "InputRightAddon",
    "InputRightElement",
    "Kbd",
    "Link",
    "LinkBox",
    "LinkOverlay",
    "List",
    "ListItem",
    "Markdown",
    "Match",
    "Menu",
    "MenuButton",
    "MenuDivider",
    "MenuGroup",
    "MenuItem",
    "MenuItemOption",
    "MenuList",
    "MenuOptionGroup",
    "Modal",
    "ModalBody",
    "ModalCloseButton",
    "ModalContent",
    "ModalFooter",
    "ModalHeader",
    "ModalOverlay",
    "Moment",
    "MultiSelect",
    "MultiSelectOption",
    "NextLink",
    "NumberDecrementStepper",
    "NumberIncrementStepper",
    "NumberInput",
    "NumberInputField",
    "NumberInputStepper",
    "Option",
    "OrderedList",
    "Password",
    "PinInput",
    "PinInputField",
    "Plotly",
    "Popover",
    "PopoverAnchor",
    "PopoverArrow",
    "PopoverBody",
    "PopoverCloseButton",
    "PopoverContent",
    "PopoverFooter",
    "PopoverHeader",
    "PopoverTrigger",
    "Progress",
    "Radio",
    "RadioGroup",
    "RangeSlider",
    "RangeSliderFilledTrack",
    "RangeSliderThumb",
    "RangeSliderTrack",
    "ResponsiveGrid",
    "ScaleFade",
    "Script",
    "Select",
    "Skeleton",
    "SkeletonCircle",
    "SkeletonText",
    "Slide",
    "SlideFade",
    "Slider",
    "SliderFilledTrack",
    "SliderMark",
    "SliderThumb",
    "SliderTrack",
    "Spacer",
    "Span",
    "Spinner",
    "Square",
    "Stack",
    "Stat",
    "StatArrow",
    "StatGroup",
    "StatHelpText",
    "StatLabel",
    "StatNumber",
    "Step",
    "StepDescription",
    "StepIcon",
    "StepIndicator",
    "StepNumber",
    "StepSeparator",
    "StepStatus",
    "StepTitle",
    "Stepper",
    "Switch",
    "Tab",
    "TabList",
    "TabPanel",
    "TabPanels",
    "Table",
    "TableCaption",
    "TableContainer",
    "Tabs",
    "Tag",
    "TagCloseButton",
    "TagLabel",
    "TagLeftIcon",
    "TagRightIcon",
    "Tbody",
    "Td",
    "Text",
    "TextArea",
    "Tfoot",
    "Th",
    "Thead",
    "Tooltip",
    "Tr",
    "UnorderedList",
    "Upload",
    "Video",
    "VisuallyHidden",
    "Vstack",
    "Wrap",
    "WrapItem",
]

_ALL_COMPONENTS += [to_snake_case(component) for component in _ALL_COMPONENTS]
_ALL_COMPONENTS += [
    "cancel_upload",
    "components",
    "color_mode_cond",
    # "custom_components",
    "desktop_only",
    "mobile_only",
    "tablet_only",
    "mobile_and_tablet",
    "tablet_and_desktop",
    "selected_files",
    "clear_selected_files",
    "EditorButtonList",
    "EditorOptions",
    "NoSSRComponent",
]

# _MAPPING: Maps module paths as keys to lists of their attributes (classes, functions, variables) as values for dynamic imports.
_MAPPING = {
    "nextpy.app": ["App", "UploadFile", "app"],
    "nextpy.backend.admin": ["AdminDash", "admin"],
    "nextpy.backend.event": [
        "EventChain",
        "background",
        "call_script",
        "clear_local_storage",
        "console_log",
        "download",
        "event",
        "prevent_default",
        "redirect",
        "remove_cookie",
        "remove_local_storage",
        "set_clipboard",
        "set_focus",
        "set_value",
        "stop_propagation",
        "upload_files",
        "window_alert",
    ],
    "nextpy.backend.middleware": ["Middleware", "middleware"],
    "nextpy.backend.route": ["route"],
    "nextpy.backend.state": ["Cookie", "LocalStorage", "State", "state", "var"],
    "nextpy.backend.vars": ["Var", "cached_var", "vars"],
    "nextpy.base": ["Base", "base"],
    "nextpy.build.compiler": ["compiler"],
    "nextpy.build.compiler.utils": ["get_asset_path"],
    "nextpy.build.config": ["Config", "DBConfig", "config"],
    "nextpy.build.testing": ["testing"],
    "nextpy.constants": ["Env", "constants"],
    "nextpy.data.jsondb": ["JsonDatabase"],
    "nextpy.data.model": ["Model", "model", "session"],
    "nextpy.frontend.components": _ALL_COMPONENTS + ["chakra", "next"],
    "nextpy.frontend.components.framer.motion": ["motion"],
    "nextpy.frontend.components.component": ["memo"],
    "nextpy.frontend.components.el": ["el"],
    "nextpy.frontend.components.moment.moment": ["MomentDelta"],
    "nextpy.frontend.components.recharts": ["recharts"],
    "nextpy.frontend.page": ["page"],
    "nextpy.frontend.style": ["color_mode", "style", "toggle_color_mode"],
    "nextpy.utils": ["utils"],
    "nextpy.frontend.components.proxy": ["animation"],
}



def _reverse_mapping(mapping: dict[str, list]) -> dict[str, str]:
    """Reverse the mapping used to lazy loading, and check for conflicting name.

    Args:
        mapping: The mapping to reverse.

    Returns:
        The reversed mapping.
    """
    reversed_mapping = {}
    for key, values in mapping.items():
        for value in values:
            if value not in reversed_mapping:
                reversed_mapping[value] = key
            else:
                console.warn(
                    f"Key {value} is present multiple times in the imports _MAPPING: {key} / {reversed_mapping[value]}"
                )
    return reversed_mapping


# _MAPPING = {value: key for key, values in _MAPPING.items() for value in values}
_MAPPING = _reverse_mapping(_MAPPING)


def _removeprefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix) :]


__all__ = [_removeprefix(mod, "nextpy.") for mod in _MAPPING]


def __getattr__(name: str) -> Type:
    """Lazy load all modules and handle custom aliases.

    Args:
        name: name of the module or attribute to load.

    Returns:
        The module or the attribute of the module.

    Raises:
        AttributeError: If the module or the attribute does not exist.
    """
    # Custom alias handling
    if name == "animation":
        module = importlib.import_module("nextpy.frontend.components.proxy")
        return module.animation


    try:
        # Check for import of a module that is not in the mapping.
        if name not in _MAPPING:
            # If the name does not start with nextpy, add it.
            if not name.startswith("nextpy") and name != "__all__":
                name = f"nextpy.{name}"
            return importlib.import_module(name)

        # Import the module.
        module = importlib.import_module(_MAPPING[name])

        # Get the attribute from the module if the name is not the module itself.
        return (
            getattr(module, name) if name != _MAPPING[name].rsplit(".")[-1] else module
        )
    except ModuleNotFoundError:
        raise AttributeError(f"module 'nextpy' has no attribute {name}") from None
