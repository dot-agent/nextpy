# Dark Mode

- Nextpy provides a straightforward mechanism to integrate a dark mode toggle, enabling users to personalize their viewing experience based on their preferences.
- The **`xt.toggle_color_mode`** function serves as the key to effortlessly implementing this visual flexibility.

```python
xt.button(
  xt.icon(tag="moon", label="Toggle Dark Mode"),  # Provide clear visual and textual cues
  on_click=xt.toggle_color_mode,
)
```

- This code example demonstrates the creation of an intuitive button with a moon icon and descriptive label, guiding users towards effortless theme switching.

### Preserving Brand Identity with Custom Colors

- Nextpy safeguards your app's unique visual character by maintaining the consistency of custom colors across both light and dark modes. This ensures a cohesive brand experience regardless of the chosen theme.
