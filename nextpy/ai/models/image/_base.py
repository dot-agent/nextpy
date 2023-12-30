# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from abc import ABC, abstractmethod


class BaseImageModel(ABC):
    @abstractmethod
    def get_image_model(self):
        pass

    @abstractmethod
    def generate_image(self, prompt: str, size: int = 512, num: int = 2):
        pass
