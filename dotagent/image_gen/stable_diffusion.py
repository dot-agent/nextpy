import os
import requests
import base64

from ._base import BaseImageLlm


class StableDiffusion(BaseImageLlm):
    def __init__(self, api_key, image_model=None, number_of_results=1, client_id=None, client_version=None):
        """
        Args:
            api_key (str): The Stability API key.
            image_model (str): The image model.
            number_of_results (int): The number of results.
            client_id (str): Client ID.
            client_version (str): Client version.
        """
        self.api_key = api_key
        self.image_model = image_model or 'stable-diffusion-xl-beta-v2-2-2'
        self.number_of_results = number_of_results
        self.api_host = os.getenv('API_HOST', 'https://api.stability.ai')
        self.url = f"{self.api_host}/v1/generation/{self.image_model}/text-to-image"
        self.client_id = client_id
        self.client_version = client_version

    def get_image_model(self):
        """
        Returns:
            str: The image model.
        """
        return self.image_model

    def generate_image(self, prompt: str, size: int = 512, style_preset='enhance', cfg_scale=7, steps=50, seed=0):
        """
        Call the Stability image API.

        Args:
            prompt (str): The prompt.
            size (int): The size.
            style_preset (str): The style preset.
            cfg_scale (int): The config scale.
            steps (int): The number of diffusion steps.
            seed (int): The seed for random noise.

        Returns:
            dict: The response.
        """
        body = {
            "width": size,
            "height": size,
            "steps": steps,
            "seed": seed,
            "cfg_scale": cfg_scale,
            "samples": self.number_of_results,
            "style_preset": style_preset,
            "text_prompts": [
                {
                "text": prompt,
                "weight": 1
                }
            ],
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        # Add client ID and version headers if provided
        if self.client_id is not None:
            headers["Stability-Client-ID"] = self.client_id
        if self.client_version is not None:
            headers["Stability-Client-Version"] = self.client_version

        response = requests.post(
            self.url,
            headers=headers,
            json=body,
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()

        for i, image in enumerate(data["artifacts"]):
            with open(f"./out/txt2img_{image['seed']}.png", "wb") as f:
                f.write(base64.b64decode(image["base64"]))

        return data
