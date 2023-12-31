##  Reference for nextpy/frontend/components/base/script(Generated by a LLM. Pending Review)

# Script Component Documentation

## Overview

The `Script` component allows developers to include external scripts in their Nextpy applications or to write inline scripts that can interact with the frontend of the application. It is commonly used for incorporating third-party JavaScript libraries, custom analytics, or dynamic interactions that are not covered by the standard Nextpy components.

## Use Cases

- Loading a third-party JavaScript library, such as D3.js for advanced data visualization.
- Adding custom JavaScript to enhance the user interface with dynamic behaviors or animations.
- Integrating analytics or tracking scripts, such as Google Analytics, to monitor application usage.
- Implementing complex client-side logic that cannot be easily replicated with existing Nextpy components.

## Anatomy

```python
from nextpy.components.base.script import Script
from nextpy.backend.vars import Var

# Inline Script example
inline_script_component = Script.create(
    "(function() { console.log('Script loaded!'); })();"
)

# External Script example
external_script_component = Script.create(
    src=Var("https://cdn.example.com/scripts/some-library.js"),
    on_load=lambda: print("Script has been loaded"),
    on_error=lambda: print("Failed to load script")
)
```

## Components

The `Script` component supports various properties and event triggers:

### Properties

| Prop Name      | Type                                    | Description                                             |
|----------------|-----------------------------------------|---------------------------------------------------------|
| src            | Optional[Union[Var[str], str]]          | The URL of the external script to be loaded.            |
| strategy       | Optional[Union[Var[str], str]]          | Strategy for when the script will execute. Options are `afterInteractive`, `beforeInteractive`, `lazyOnload`. |
| style          | Optional[Style]                         | The style definitions for the component.                |
| key            | Optional[Any]                           | A unique key that identifies the component in the DOM.  |
| id             | Optional[Any]                           | The DOM id for the component.                           |
| class_name     | Optional[Any]                           | The class name for the component.                       |
| autofocus      | Optional[bool]                          | If set, the component takes focus when the page loads.  |
| custom_attrs   | Optional[Dict[str, Union[Var, str]]]    | Custom attributes for the component.                    |

### Event Triggers

| Event Trigger     | Type                                                     | Description                                                               |
|-------------------|----------------------------------------------------------|---------------------------------------------------------------------------|
| on_blur           | Optional[Union[EventHandler, EventSpec, list, function]] | Event handler triggered when the component loses focus.                   |
| on_click          | Optional[Union[EventHandler, EventSpec, list, function]] | Event handler triggered on a click event.                                 |
| on_error          | Optional[Union[EventHandler, EventSpec, list, function]] | Event handler triggered if the script fails to load.                      |
| on_load           | Optional[Union[EventHandler, EventSpec, list, function]] | Event handler triggered after the script has finished loading.            |
| on_ready          | Optional[Union[EventHandler, EventSpec, list, function]] | Event handler triggered after the script has loaded and on each mount.    |
| on_mouse_down     | Optional[Union[EventHandler, EventSpec, list, function]] | Event handler triggered on a mouse down event.                            |
| on_mouse_up       | Optional[Union[EventHandler, EventSpec, list, function]] | Event handler triggered on a mouse up event.                              |
| on_unmount        | Optional[Union[EventHandler, EventSpec, list, function]] | Event handler triggered before the component is removed from the DOM.     |
| ...               | ...                                                      | Other standard mouse and focus events.                                    |

## Notes

- Inline scripts are executed once they are mounted in the DOM.
- The `src` property is required if you are not providing an inline script.
- Ensure that any external scripts you load comply with content security policies and do not violate any cross-origin restrictions.

## Best Practices

- When adding third-party scripts, consider the implications on performance and security. Use the `strategy` property to control when the script loads.
- Keep inline scripts minimal to avoid performance bottlenecks.
- Utilize the `on_error` event trigger to handle cases where external scripts fail to load and provide fallback functionality.
- Use the `on_ready` event to initialize any JavaScript functionality that depends on the loaded script.