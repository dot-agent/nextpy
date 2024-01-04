# Asset Management

In your Nextpy project, the "assets/" folder functions as a dedicated repository for various static assets contributing to your application's functionality and aesthetics. Here's a breakdown of the assets it typically accommodates:

- **Images:** Visual elements like logos, product photos, background images, and graphics enhancing the visual appeal and user experience.
- **Stylesheets (CSS):** Files with style rules defining the presentation of your app's elements, ensuring a cohesive and visually appealing design.
- **Icons:** Small, symbolic images for navigation, actions, or visual cues, enhancing clarity and interactivity.
- **Other Static Resources:** This category includes diverse asset types like:
  - **Fonts:** Custom fonts contributing to a unique visual style and enhancing readability.
  - **Audio files:** Sound effects and background music enriching the user experience and providing auditory feedback.
  - **Video files:** Animations or video content that can be integrated for dynamic and engaging experiences.
  - **JSON files:** Data files storing structured information accessed and utilized within your app's logic.

## Organization

Consider structuring the "assets/" folder with subfolders for different asset types (e.g., "images/", "stylesheets/", "icons/") to maintain organization and clarity.

## Accessing Assets

- All assets are stored within the dedicated `assets/` directory inside your Nextpy project.
- Each asset's path within this directory serves as its unique identifier.

## Using Assets

- Using assets into your code by referencing their relative path from the `assets/` directory.
- Use the appropriate function based on the asset type, such as `xt.image` for images and `xt.link` for external files.

## Example

To display an image named `nextpy_logo.png` located in the `assets/` directory, use the following code:

```python
xt.image(src="/nextpy_logo.png", width="100px")
```
> [!TIP]
>The relative path is from the "assets/" directory, so no need to include "assets/" in the source path.

### Favicon

- The favicon is a small icon displayed in the browser tab associated with your app.
- Place your favicon file (typically a `.ico` or `.png`) within the `assets/` directory.
- Nextpy automatically uses the favicon file for display.
  
```python

xt.link(
    xt.box(
        xt.image(src="favicon.ico", width=30, height="auto"),
        border_radius="6",
        bg="#F0F0F0",
    ),
    href="/",
)
```


## Downloading Files

Nextpy allows users to download files from your server, and two methods are available:

1. **xt.link:** Use simple HTML links for direct file download:

```python
xt.link("Download", href="/golden_shield.png")
```

2. **xt.download:** Implement a button and utilize the `xt.download` function for more control:

```python
xt.button(
    "Download File",
    on_click=xt.download(url="/mystic_scroll.pdf")
)
```

## Customizing Downloaded Filenames

- The `xt.download` function can rename downloaded files:

```python
xt.button(
    "Download & Rename",
    on_click=xt.download(url="/potion.png", filename="elixir_of_power.png")
)
```

## Uploading Files

Enable users to upload files to your server using the `xt.upload` function:

```python
def index():
    return xt.box(
        xt.upload(
            xt.text("Drag and drop files here or click to upload.")
        )
    )
```
