##  Reference for nextpy/frontend/components/core/upload.pyi

# Nextpy Documentation - Upload Component

## Upload Component

The `Upload` component in Nextpy is designed to provide a user-friendly interface for uploading files within a full-stack Python application. It supports features like drag-and-drop, multiple file uploads, and file type restrictions.

### Anatomy

#### Basic Usage

To use the `Upload` component, create an instance and add it to your application layout. Here is a simple example to include an upload button:

```python
from nextpy.components.core import Upload

# Create an Upload component with basic settings
upload = Upload.create()

# Add the upload component to your app layout
app.layout = upload
```

#### Advanced Usage

You can customize the `Upload` component by specifying various parameters such as accepted file types, maximum file size, or the maximum number of files:

```python
from nextpy.components.core import Upload

# Specify accepted file types and limits
upload = Upload.create(
    accept={'image/*': ['.png', '.jpg', '.jpeg', '.gif']},
    max_files=5,
    max_size=10*1024*1024,  # 10MB
    multiple=True
)

# Add the upload component to your app layout
app.layout = upload
```

### Components

**Upload**: Main component that users interact with to upload files.

**UploadFilesProvider**: A provider component that manages the state of files being uploaded within its scope.

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

Remember to adhere to accessibility and security best practices when implementing file upload features in your application.