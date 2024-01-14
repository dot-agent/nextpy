## xt.upload

**What's it do?**

- Lets users upload files from their device to your app.
- You can customize xt.upload's appearance and behavior to fit your needs.

**How to Use It:**
![image](https://res.cloudinary.com/doojikdqd/image/upload/v1705216797/Docs/ref-upload_oc4n8c.png)


1. **Add it to your view:**
   Create a simple upload area in your app:

   ```python
   xt.upload(
       xt.text("Drag and drop files here or click to select files"),
   ),
   ```

2. **Customize its look and feel (optional):**
   - **Content:** Add informative text, buttons, or other components within it.
   - **Styling:** Apply borders, padding, and colors to align with your app's design.

   ```python
   xt.upload(
       xt.text("Drag and drop files here or click to select files"),
       border="1px dotted rgb(107,99,246)",
       padding="2em",
   ),
   ```

3. **Control what's uploaded:**
   - **Accepted file types:** Specify using the `accept` property (e.g., `accept={'image/*': ['.png', '.jpg', '.jpeg', '.gif']}`).
   - **File limits:** Set maximum file size and number of files using `max_size` and `max_files`.
   - **Multiple files:** Enable simultaneous uploads with `multiple=True`.

   ```python
   xt.upload(
       accept={'image/*': ['.png', '.jpg', '.jpeg', '.gif']},
       max_files=5,
       max_size=10*1024*1024,  # 10MB
       multiple=True
   )
   ```

4. **Handle file uploads:**
   - **Event handler creation:** Craft a function to process the selected files.
   - **Trigger binding:** Attach this function to a trigger, such as a button's `on_click` event.
   - **File access:** Retrieve uploaded files within the handler using `xt.upload_files()`.

   ```python
   import nextpy as xt

   class State(xt.State):
       """The app state."""
       
       img: list[str]  # The images to show.

       async def handle_upload(self, files: list[xt.UploadFile]):
           """Handle the upload of file(s).

           Args:
               files: The uploaded files.
           """
           for file in files:
               upload_data = await file.read()
               outfile = xt.get_asset_path(file.filename)

               # Save the file.
               with open(outfile, "wb") as file_object:
                   file_object.write(upload_data)

               # Update the img var.
               self.img.append(file.filename)


   def index():
       """The main view."""
       return xt.vstack(
           xt.upload(
               xt.text("Drag and drop files here or click to select files"),
               border="1px dotted rgb(107,99,246)",
               padding="2em",
               multiple=True,
               accept={
                  "application/pdf": [".pdf"],
                  "image/jpeg": [".jpg", ".jpeg"],
                  "image/gif": [".gif"],
                  "image/png": [".png"],
                  "image/webp": [".webp"],
                  "text/html": [".html", ".htm"],
               },
               max_files=5,
           ),
           xt.hstack(xt.foreach(xt.selected_files, xt.text)),
           xt.button(
               "Upload",
               on_click=lambda: State.handle_upload(xt.upload_files()),
           ),
           xt.button(
               "Clear",
               on_click=xt.clear_selected_files,
           ),
           xt.foreach(
               State.img,
               lambda img: xt.image(src=img)
           ),
       )

   # Create the app.
   app = xt.App()
   app.add_page(index)
   ```

**Customizable Properties:**
#### Properties Table

| Prop Name   | Type                           | Description                                                 |
|-------------|--------------------------------|-------------------------------------------------------------|
| accept      | `Dict[str, List]`              | Specifies the types of files that the server accepts.       |
| disabled    | `bool`                         | If `True`, disables the component.                          |
| max_files   | `int`                          | Maximum number of files that can be uploaded at once.       |
| max_size    | `int`                          | Maximum size for a file in bytes.                           |
| min_size    | `int`                          | Minimum size for a file in bytes.                           |
| multiple    | `bool`                         | Allows multiple files to be selected if `True`.             |
| no_click    | `bool`                         | Disables the click event to trigger file upload.            |
| no_drag     | `bool`                         | Disables the drag-and-drop feature.                         |
| no_keyboard | `bool`                         | Disables keyboard interaction for triggering file upload.   |
| style       | `Style`                        | Custom CSS styles for the component.                        |

#### Event Triggers

- `on_drop`: Triggered when files are dropped into the dropzone.
- `on_click`: Triggered when the component is clicked.
- More event triggers can be implemented based on the app's requirements.

### Notes

- Ensure that the `accept` prop follows the correct format for specifying MIME types.
- For security reasons, it's essential to validate the uploaded files on the server side.

### Best Practices

- Always use the `UploadFilesProvider` to wrap around areas where files will be uploaded to manage the state properly.
- Customize the appearance of the upload area with CSS to align with your application's theme.
- Provide feedback to the user upon successful or failed uploads through event handlers.

---
