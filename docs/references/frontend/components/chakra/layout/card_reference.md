##  Reference for nextpy/frontend/components/chakra/layout/card(Generated by a LLM. Pending Review)

# Nextpy Card Component Documentation

## Card

### Overview

The `Card` component in Nextpy is a versatile UI building block that allows you to create structured sections of content. It is a common design pattern used to group related content and actions, making them easier to read and interact with. Cards are typically used to display a variety of content types, such as text, images, and actions.

### Use Cases

- Displaying a user profile with an avatar, name, and additional details.
- Showcasing a product with an image, description, and purchase options.
- Organizing a blog post preview with a title, summary, and a "read more" link.

### Anatomy

A `Card` can include a `header`, a `body`, and a `footer`. Each part serves a specific purpose:

- **Header (`CardHeader`)**: A top section that often contains the title or summary.
- **Body (`CardBody`)**: The main content area for detailed information.
- **Footer (`CardFooter`)**: A bottom section for actions or supplementary information.

#### Basic Implementation

```python
from nextpy.components.chakra.layout.card import Card, CardHeader, CardBody, CardFooter

card = Card.create(
    header=CardHeader.create("Card Title"),
    body=CardBody.create("This is the main content of the card."),
    footer=CardFooter.create("Footer content")
)
```

#### Advanced Implementation

```python
from nextpy.components.chakra.layout.card import Card, CardHeader, CardBody, CardFooter
from nextpy.frontend.style import Style

header_style = Style(background_color="blue.500", color="white")
body_style = Style(padding="4")
footer_style = Style(padding="2", border_top="1px solid", border_color="gray.200")

card = Card.create(
    header=CardHeader.create("Advanced Card Title", style=header_style),
    body=CardBody.create("Detailed information can go here.", style=body_style),
    footer=CardFooter.create("Links or actions here.", style=footer_style)
)
```

### Components

#### CardHeader

- **Purpose**: To display the title or introductory content of a card.
- **Properties**:
  
  | Prop Name      | Type    | Description                                      |
  |----------------|---------|--------------------------------------------------|
  | `style`        | `Style` | Custom style for the header.                     |
  | `on_click`     | `Event` | Event triggered when the header is clicked.      |
  | `custom_attrs` | `Dict`  | Custom attributes for additional HTML properties |

#### CardBody

- **Purpose**: To contain the main content or body of the card.
- **Properties**:
  
  | Prop Name      | Type    | Description                                      |
  |----------------|---------|--------------------------------------------------|
  | `style`        | `Style` | Custom style for the body.                       |
  | `on_scroll`    | `Event` | Event triggered when the body is scrolled.       |
  | `custom_attrs` | `Dict`  | Custom attributes for additional HTML properties |

#### CardFooter

- **Purpose**: To provide a space for actions or supplementary information.
- **Properties**:
  
  | Prop Name      | Type    | Description                                      |
  |----------------|---------|--------------------------------------------------|
  | `style`        | `Style` | Custom style for the footer.                     |
  | `on_mouse_up`  | `Event` | Event triggered when a mouse button is released. |
  | `custom_attrs` | `Dict`  | Custom attributes for additional HTML properties |

### Notes

- Avoid overloading the card with too much information or too many actions.
- For accessibility, ensure that the `Card` and its components are navigable and actionable via keyboard controls.

### Best Practices

- Maintain a consistent design language for cards throughout your application.
- Use padding and margins responsibly to keep the content readable and aesthetically pleasing.
- Consider using shadows or borders to distinguish the card from the rest of the content on the page.
- Use the `style` prop to customize the appearance of the card to fit the design of your application.

By following these guidelines and utilizing the `Card` component, you can create clean, organized, and user-friendly interfaces in your full-stack Python applications with Nextpy.