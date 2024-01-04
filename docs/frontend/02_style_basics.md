# Styling Overview

Styling is a crucial aspect of creating visually appealing apps. Nextpy offers multiple ways to inte style into your components, ranging from global application styles to inline component-specific styles. Additionally, Nextpy supports the use of Tailwind CSS, providing a vast array of utility classes for more intricate design control.  
   
In nextpy, styles can be applied through three distinct approaches: global styles that affect all components, component-specific styles that target particular types of components, and inline styles that are specific to individual component.

## 1. Global Styles  
   - Apply to the entire application for consistency.
   - Defined in a separate file (e.g., `styles.py`).
   - Passed to the `xt.App` constructor as a Python dictionary. 
   
```python  
style = {
    "background_color": "green",
    "font_weight": "bold"
}
app = xt.App(style=style)
```  
   
## 2. Component Styles  
   - Set default styles for specific component types.
   - Defined in a separate file as a Python dictionary.
   - Use component selectors (e.g., `xt.button`) to target styles. 
   

```python  
# Style dictionary with a component selector. Notice the selector xt.Button:
style = {
  xt.button: {
    "background_color": "green",
    "font_weight": "bold"
  },
}

app = xt.App(style=style)
```  
   
## 3. Inline Styles  
   - Apply unique styles to individual component instances.
   - Defined directly within the component's arguments.
   - Override global and component styles.
 
   

```python  
# Notice the color green is defined with in the component itself. 
xt.button(
    "Welcome to Nextpy",
    color="green",
)
```  
   
## Style Precedence  
In the world of Nextpy styling, inline styles reign supreme, taking precedence over component and global styles. This hierarchy enables a flexible approach to styling customization.  
   
   
## 4. Tailwind CSS Integration  
Tailwind CSS throws away bulky CSS files and introduces a collection of atomic classes that represent individual CSS properties. You simply combine these classes to build the styles you need. This leads to several benefits:

- Rapid Prototyping: Forget writing lengthy CSS declarations; quickly apply styles and iterate on your design.
- Consistent Design: Tailwind's built-in theme and spacing system ensure a cohesive visual language across your app.

```python
config = AppConfig(
    app_name="nextpy_app",
    tailwind={},
)

```
   
### Configuration support for tailwind
We have comprehensive support for Tailwind customization and streamlines plugin and preset usage:

- Full Configuration Support: Access the full range of Tailwind configuration options to tailor the framework to your project's unique needs.
- Automatic Wrapping for Plugins and Presets: We automatically handle the require() statements for plugins and presets within your configuration, eliminating manual wrapping and simplifying setup.

```python  
config = AppConfig(  
    app_name="nextpy_app",  
    tailwind={  
        "theme": {  
            "extend": {},  
        },  
        "plugins": ["@tailwindcss/typography"],  
    },  
)  
```  
   
Tailwind's utility classe names can be seamlessly utilized through the `class_name` property.  
   
### Using Tailwind Classe Names
```python  
xt.box(  
    "Hello World",  
    class_name="text-sm italic text-gray-900",  
)  
```  
   
For more insights, explore the [Tailwind CSS documentation](https://tailwindcss.com/docs/font-style) or this handy [Tailwind CSS cheatsheet](https://umeshmk.github.io/Tailwindcss-cheatsheet/).  
   
### Disabling Tailwind CSS  
Opting out of Tailwind CSS is as easy as changing an outfit—simply set the `tailwind` option to `None`.  
   
```python  
config = AppConfig(  
    app_name="nextpy_app",  
    tailwind=None,  
)  
```  
   
> [!TIP]
> **Pythonic Conventions**: Utilize snake_case for CSS property names within styling dictionaries (e.g., `font_size` instead of `fontSize`).

> **Class Names and IDs**: Use dashes or camelCase for class names and IDs to maintain consistency. Nextpy automatically adapts snake_case identifiers to camelCase for styling purposes.

> **External Libraries**: For external libraries with underscored class names, reference external stylesheets or adapt the identifiers as needed.  
   

 ## Style Props: Reusable Style Dictionaries

In Nextpy, you can directly apply styles to elements using the `style` prop, promoting a cleaner and more organized approach to styling. Here's how it works:

**Benefits:**

- **Reusability:** Eliminate redundant styling code.
- **Consistency:** Maintain a cohesive look and feel.
- **Organization:** Better code structure and maintainability.
- **Flexibility:** Easily combine and override styles as needed.

**Creating Reusable Style Dictionaries:**

- Define style dictionaries with CSS properties as keys and desired values:

```python
text_style = {
    "color": "green",
    "font_family": "Comic Sans MS",
    "font_size": "1.2em",
    "font_weight": "bold",
    "box_shadow": "rgba(240, 46, 170, 0.4) 5px 5px, rgba(240, 46, 170, 0.3) 10px 10px"
}
```

**Applying Styles to Multiple Elements:**

- Use the `style` prop to apply the dictionary to components:

```python
xt.vstack(
    xt.text("Hello", style=text_style),
    xt.text("World", style=text_style),
)
```

**Combining and Overriding Styles:**

- Pass a list of style dictionaries to the `style` prop for merging:

```python
style1 = {
    "color": "green",
    "font_family": "Comic Sans MS",
    "border_radius": "10px",
    "background_color": "rgb(107,99,246)",
}
style2 = {
    "color": "white",
    "border": "5px solid #EE756A",
    "padding": "10px",
}

xt.box(
    "Multiple Styles",
    style=[style1, style2],  # style2 overrides overlapping properties
)
```


## Pseudo-Classes

We supports all of chakra's pseudo-classes, it's a powerful CSS feature that allows you to style components based on their state or user interactions without using xt.State. Here's a breakdown of how they work:

### Understanding Pseudo-Classes

- **What They Are:** Pseudo-classes are keywords added to selectors to target elements in specific states, such as hover, focus, active, and more.
- **Why They Matter:** They enable you to create interactive and engaging UIs that respond to user actions, enhancing visual feedback and usability.

### Applying Pseudo-Classes

1. **Using the Underscore Prefix:** Pass a dictionary of styles to a component's constructor, with the key being the pseudo-class prefixed with an underscore (e.g., `_hover`, `_focus`).
2. **Value as Style Dictionary:** The value of this key is another dictionary containing the CSS properties and values you want to apply when the pseudo-class is activated.

**Example:**

```python
xt.box(
    xt.text("Hover Me", _hover={"color": "red"}),
    class_name="text-4xl text-center text-blue-500"
)
```

**In this example:**

- The text will be blue initially.
- When the user hovers over it, the `_hover` styles activate, turning the text red.

**Common Pseudo-Classes:**

- `_hover`: Styles for when the user hovers over an element.
- `_focus`: Styles for when an element is focused (e.g., a text input).
- `_active`: Styles for when an element is actively being used (e.g., a pressed button).
- `_disabled`: Styles for disabled elements.
