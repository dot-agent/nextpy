# Monday Loader

This loader loads data from monday.com. The user specifies an API token to initialize the MondayReader. They then specify a monday.com board id to load in the corresponding DocumentNode objects.

## Usage

Here's an example usage of the MondayReader.

```python
from nextpy.ai import download_loader

MondayReader = download_loader('MondayReader')

reader = MondayReader("<monday_api_token>")
documents = reader.load_data("<board_id: int>")

```

Check out monday.com API docs - [here](https://developer.monday.com/apps/docs/mondayapi)


