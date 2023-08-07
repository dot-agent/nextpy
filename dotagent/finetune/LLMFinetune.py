from abc import ABC, abstractmethod
from logging import Logger
import openai

class LLMFinetune(ABC):
    def __init__(self, logger: Logger, openai_key: str):
        self.logger = logger
        openai.api_key = openai_key

    @abstractmethod
    def transform_data(self, train_csv_file: str, val_csv_file: str , train_output_file: str, val_output_file: str) -> str:
        pass

    @abstractmethod
    def finetune(self, **kwargs):
        pass
