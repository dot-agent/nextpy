# OpenAI DALL-E Image Generation

This is a simple Python interface for generating images using OpenAI's DALL-E model.

## Prerequisites

Ensure you have the `openai` Python library installed. If not, you can install it using pip:

```bash
pip install openai
```
# Usage Dalle

```python

# Define your API key and any other settings
api_key = 'your-api-key-here'
image_model = 'your-image-model-here'  # Optional
number_of_results = 5  # Optional, default is 1

# Create an instance of the OpenAiDalle class
dalle = OpenAiDalle(api_key, image_model, number_of_results)

# Define a prompt and image size
prompt = 'A beautiful sunset over the mountains'
size = 512  # Optional, default is 512

# Generate an image
response = dalle.generate_image(prompt, size)

# Print the response
print(response)
```
# Usage

```python

# Define your API key and any other settings
api_key = 'your-api-key-here'
image_model = 'your-image-model-here'  # Optional
number_of_results = 5  # Optional, default is 1
client_id = 'your-client-id-here'  # Optional
client_version = 'your-client-version-here'  # Optional

# Create an instance of the StableDiffusion class
image_llm = StableDiffusion(api_key, image_model, number_of_results, client_id, client_version)

# Define a prompt and image size
prompt = 'A beautiful sunset over the mountains'
size = 512  # Optional, default is 512

# Define other settings
style_preset = 'enhance'  # Optional, default is 'enhance'
cfg_scale = 7  # Optional, default is 7
steps = 50  # Optional, default is 50
seed = 0  # Optional, default is 0

# Generate an image
response = image_llm.generate_image(prompt, size, style_preset, cfg_scale, steps, seed)

# Print the response
print(response)
```