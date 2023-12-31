##  Reference for nextpy/frontend/components/radix/primitives/form(Generated by a LLM. Pending Review)

# Nextpy Documentation: Form Components

## FormComponent

**Overview**: `FormComponent` serves as the base class for all form-related components, providing common functionalities and properties that are shared by its subclasses, such as form fields, labels, and submit buttons.

**Use Cases**: It is used internally within the Nextpy library to create form components that manage user input, validation, and form submission.

**Structure and Usage**:
- Inherits from `RadixPrimitiveComponent`.
- Not intended to be used directly by developers.
- Shared properties and methods are inherited by all form-specific components.

## FormRoot

**Overview**: `FormRoot` is the component that wraps the entire form. It handles the form submission, including data gathering and validation.

**Anatomy**:
- Basic Usage:
```python
form = FormRoot.create(
    form_field(name="username"),
    form_field(name="password"),
    form_submit(),
    on_submit=handle_form_submit
)
```
- Advanced Usage: 
```python
form = FormRoot.create(
    form_field(name="username"),
    form_field(name="password"),
    form_submit(),
    reset_on_submit=True,  # Clears the form on submit
    on_submit=handle_form_submit,
    style=my_custom_style,
    custom_attrs={"data-qa": "user-form"}
)
```

**Components**:
- `reset_on_submit` (bool): Clears the form when set to `True` after submission.
- `handle_submit_unique_name` (str): A unique name to distinguish this form's submit handler when there are multiple forms.

**Notes**: 
- Always provide an `on_submit` event handler to process form data.

**Best Practices**:
- Utilize the `reset_on_submit` property for forms that should clear after submission.

## FormField

**Overview**: `FormField` represents a single input field within a form, responsible for collecting user input.

**Anatomy**:
- Basic Usage:
```python
field = FormField.create(
    form_label("Username"),
    form_control(as_child=True, children=[
        Tag.input(type="text", name="username")
    ]),
    form_message(match="valueMissing", children=["This field is required"]),
    name="username"
)
```

**Components**:
- `name` (str): The name attribute for the form field, which is used to reference form data.

**Notes**: 
- `FormField` does not include an input element by default; it must be added as a child.

**Best Practices**:
- Always provide a `name` attribute to ensure the field data can be collected on form submission.

## FormLabel

**Overview**: `FormLabel` provides a label for a `FormField`.

**Anatomy**:
- Basic Usage:
```python
label = FormLabel.create(children=["Username"])
```

**Components**: N/A

**Notes**: 
- `FormLabel` should be used within a `FormField` for accessibility and usability.

## FormControl

**Overview**: `FormControl` is used to contain the actual input control (like an `<input>`, `<select>`, or `<textarea>`) within a `FormField`.

**Anatomy**:
- Basic Usage:
```python
control = FormControl.create(
    as_child=True, 
    children=[Tag.input(type="text", name="username")]
)
```

**Components**: N/A

**Notes**: 
- Use `as_child=True` when embedding native HTML tags like `<input>`.

## FormMessage

**Overview**: `FormMessage` displays validation or informative messages related to a form field.

**Anatomy**:
- Basic Usage:
```python
message = FormMessage.create(
    match="valueMissing", 
    children=["Please enter your username."]
)
```

**Components**:
- `match` (LiteralMatcher): Specifies the validity state that triggers the message display.
- `forceMatch` (bool): Forces the message to be displayed, useful for server-side validation.

**Notes**: 
- Should be used within `FormField` to provide contextual messages for user input.

## FormValidityState

**Overview**: `FormValidityState` is a component that allows developers to conditionally render content based on the validity state of a form or field.

**Anatomy**:
- Usage: Typically used internally and not directly exposed to developers.

## FormSubmit

**Overview**: `FormSubmit` is a button or control used to submit the form.

**Anatomy**:
- Basic Usage:
```python
submit_button = FormSubmit.create(children=["Submit"])
```

**Components**: N/A

**Notes**: 
- Typically used within `FormRoot` to provide a submission mechanism for the form.

**Best Practices**:
- Always include a `FormSubmit` within `FormRoot` to allow users to submit the form.

The above documentation provides a concise, clear, and complete guide to using form-related components in Nextpy. It includes practical examples, highlights important considerations, and offers best practice advice, catering to a wide range of developers.