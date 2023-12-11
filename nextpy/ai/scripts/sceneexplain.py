# New code implementation for the following api different from langchain approach

"""Util that calls SceneXplain.

In order to set this up, you need API key for the SceneXplain API.
You can obtain a key by following the steps below.
- Sign up for a free account at https://scenex.jina.ai/.
- Navigate to the API Access page (https://scenex.jina.ai/api) and create a new API key.
"""
import base64
import http
import json
from typing import Dict

from pydantic import BaseModel, BaseSettings, Field, root_validator

from nextpy.utils.data_ops import get_from_dict_or_env


def _image_to_data_uri(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded_image}"


class SceneXplainAPIWrapper(BaseSettings, BaseModel):
    """Wrapper for SceneXplain API.

    In order to set this up, you need API key for the SceneXplain API.
    You can obtain a key by following the steps below.
    - Sign up for a free account at https://scenex.jina.ai/.
    - Navigate to the API Access page (https://scenex.jina.ai/api)
      and create a new API key.
    """

    scenex_api_key: str = Field(..., env="SCENEX_API_KEY")
    scenex_api_url: str = "us-central1-causal-diffusion.cloudfunctions.net"

    def _describe_image(self, image: str) -> str:
        local_image_path = image
        data = {
            "data": [
                {"image": _image_to_data_uri(local_image_path), "features": []},
            ]
        }

        headers = {
            "x-api-key": f"token {self.scenex_api_key}",
            "content-type": "application/json",
        }

        connection = http.client.HTTPSConnection(
            "us-central1-causal-diffusion.cloudfunctions.net"
        )
        connection.request("POST", "/describe", json.dumps(data), headers)
        response = connection.getresponse()
        response_data = response.read().decode("utf-8")
        response_data = json.loads(response_data)
        output = response_data["result"][0]["text"]
        connection.close()
        return output

    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key exists in environment."""
        scenex_api_key = get_from_dict_or_env(
            values, "scenex_api_key", "SCENEX_API_KEY"
        )
        values["scenex_api_key"] = scenex_api_key

        return values

    def run(self, image: str) -> str:
        """Run SceneXplain image explainer."""
        description = self._describe_image(image)
        if not description:
            return "No description found."

        return description
