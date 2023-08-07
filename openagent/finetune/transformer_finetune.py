from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
from logging import Logger
import openai
from . import LLMFinetune

class TransformersFinetune(LLMFinetune):
    def __init__(self, logger: Logger, base_model: str):
        super().__init__(logger, openai_key=None)
        self.model = AutoModelForCausalLM.from_pretrained(base_model)
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)

    def transform_data(self, train_csv_file: str, val_csv_file: str, train_output_file: str, val_output_file: str) -> str:
        # Implement logic to transform CSV files to desired JSON or other formats
        # You can load, process, and save the CSV data here
        # Return the path or message confirming the transformation
        pass

    def finetune(self, data_path, output_dir, num_epochs=1, batch_size=32, learning_rate=5e-5, val_set_size=0.1, max_length=512):
        # Load dataset
        data = load_dataset("json", data_files={"train": data_path})

        # Split data into training and validation sets
        train_val = data["train"].train_test_split(test_size=val_set_size, shuffle=True, seed=42)
        train_data = train_val["train"]
        valid_data = train_val["test"]

        # Tokenization function
        def tokenize_function(examples):
            return self.tokenizer(examples["text"], truncation=True, max_length=max_length, padding="max_length")

        # Tokenize dataset
        train_data = train_data.map(tokenize_function, batched=True)
        valid_data = valid_data.map(tokenize_function, batched=True)

        # Training arguments
        training_args = TrainingArguments(
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=num_epochs,
            learning_rate=learning_rate,
            output_dir=output_dir,
            evaluation_strategy="steps" if val_set_size > 0 else "no",
            logging_dir='./logs',
        )

        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_data,
            eval_dataset=valid_data,
        )

        # Training
        trainer.train()

        # Save model
        self.model.save_pretrained(output_dir)
