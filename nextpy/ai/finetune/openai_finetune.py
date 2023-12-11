import csv
import json
import logging
import time
from logging import Logger
from typing import List, Optional

import openai

from . import LLMFinetune

# openai.organization = "YOUR_ORG_ID"
# APIKEY
# openai.Model.list()


class OpenaiFinetune(LLMFinetune):
    def __init__(self, logger: Logger, openai_key: str):
        self.logger = logger
        openai.api_key = openai_key

    def transform_data(
        self,
        train_csv_file: str,
        val_csv_file: str,
        train_output_file: str,
        val_output_file: str,
        llm_model: str = "openai",
    ) -> str:
        """Transforms CSV files into JSONL and creates files for fine-tuning."""
        # Verify llm_model
        if llm_model != "openai":
            raise ValueError("Unsupported model:", llm_model)

        # Paths and Output files
        paths = [train_csv_file, val_csv_file]
        output_files = [train_output_file, val_output_file]

        # Extracting prompt-completion pairs
        prompt_completion_pairs = []
        for csv_file in paths:
            with open(csv_file, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        prompt = row[0]
                        completion = row[1]
                        prompt_completion_pairs.append((prompt, completion))

        # Writing to JSONL
        for output_file, pairs in zip(output_files, prompt_completion_pairs):
            with open(output_file, "w") as f:
                for pair in pairs:
                    json_obj = {"prompt": pair[0], "completion": pair[1]}
                    json_str = json.dumps(json_obj)
                    f.write(json_str + "\n")

        # Creating Files
        ids = []
        for output_file in output_files:
            if not output_file.endswith(".jsonl"):
                raise Exception(
                    "args `output_file` must be the **file** path to the .jsonl file"
                )
            try:
                _ = openai.File.create(
                    file=open(output_file, "rb"), purpose="fine-tune"
                )
                ids.append(_)
            except Exception as e:
                self.logger.error(f"Error creating file: {e}")
                raise e

        return output_files, ids

    # TODO: Specify use of the method
    # def model(
    #     self,
    #     model_name: str,
    #     input: str,
    #     instruction: str,
    #     n: int,
    #     temperature: float,
    #     top_p: float,
    # ):
    #     try:
    #         model = openai.Edit.create(
    #             model=model_name,
    #             temperature=temperature,
    #             top_p=top_p,
    #             input=input,
    #             instruction=instruction,
    #             n=n,
    #         )
    #         return model
    #     except Exception as e:
    #         self.logger.error(f"Error creating model: {e}")
    #         raise e

    def finetune(
        self,
        training_file: str,
        model_name: Optional[str] = "curie",
        n_epoch: Optional[int] = 4,
        validation_file: Optional[str] = None,
        batch_size: Optional[int] = None,
        learning_rate_multiplier: Optional[int] = None,
        prompt_loss_weight: Optional[int] = 0.01,
        compute_classification_metrics: Optional[bool] = False,
        classification_n_classes: Optional[int] = None,
        classification_positive_class: Optional[str] = None,
        classification_betas: Optional[List[float]] = None,
        suffix: Optional[str] = None,
    ):
        """_summary_.

        Args:
            training_file (str): The ID of an uploaded file that contains training data.
            model_name (Optional[str], optional): The name of the base model to fine-tune. You can select one of "ada", "babbage", "curie", "davinci", or a fine-tuned model created after 2022-04-21. Defaults to "curie".
            n_epoch (Optional[int], optional):  Number of epochs to train the model for. Defaults to 4.
            validation_file (Optional[str], optional): The ID of an uploaded file that contains validation data. Defaults to None.
            batch_size (Optional[int], optional): Batch size to use for training. Defaults to None.
            learning_rate_multiplier (Optional[int], optional): Learning rate multiplier to use for training. Defaults to None.
            prompt_loss_weight (Optional[int], optional): Weight to use for loss on the prompt tokens. Defaults to 0.01.
            compute_classification_metrics (Optional[bool], optional): If True, classification metrics such as accuracy and f1-score are computed for validation set. Defaults to False.
            classification_n_classes (Optional[int], optional): Number of classes in a classification task. Defaults to None.
            classification_positive_class (Optional[str], optional): This parameter is needed to generate precision, recall, and F1 metrics when doing binary classification. Defaults to None.
            classification_betas (Optional[List[float]], optional): If this is provided, we calculate F-beta scores at the specified beta values. Defaults to None.
            suffix (Optional[str], optional): A string of up to 40 characters that will be added to your fine-tuned model name. Defaults to None.

        Raises:
            e: Errors generated while creating fine-tune job
            Exception: If fine-tuning job fails

        Returns:
            _type_: _description_
        """
        # openai.FineTune.create(training_file="file-XGinujblHPwGLSztz8cPS8XY")

        job_id = None
        try:
            job_id = openai.FineTune.create(
                training_file=training_file,
                model=model_name,
                n_epochs=n_epoch,
                validation_file=validation_file,
                batch_size=batch_size,
                learning_rate_multiplier=learning_rate_multiplier,
                prompt_loss_weight=prompt_loss_weight,
                compute_classification_metrics=compute_classification_metrics,
                classification_n_classes=classification_n_classes,
                classification_positive_class=classification_positive_class,
                classification_betas=classification_betas,
                suffix=suffix,
            )
            while openai.FineTune.retrieve(job_id.get("id")).get("status") == "pending":
                time.sleep(1)
                self.logger.info(
                    "Fine-tuning job status: %s",
                    openai.FineTune.retrieve(job_id.get("id")).get("status"),
                )

            if openai.FineTune.retrieve(job_id.get("id")).get("status") == "failed":
                self.logger.error("Fine-tuning job failed")
                raise Exception("Fine-tuning job failed")

            self.logger.info("Fine-tuning job completed successfully")
            return job_id

        except Exception as e:
            self.logger.error(f"Error creating fine-tune job: {e}")
            raise e


if __name__ == "__main__":
    from creds import OPENAI_KEY

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    finetune = Finetune(logger, openai_key=OPENAI_KEY)
    train_path, val_path = finetune.generate_jsonl_from_csv(
        "sports_train.csv", "sports_val.csv", "sports_train.jsonl", "sports_val.jsonl"
    )
    output_paths, ids = finetune.create_file(output_files=[train_path, val_path])
    train_file, val_file = output_paths
    train_id, val_id = ids
    job_id = finetune.finetune(
        training_file=train_id.get("id"),
        n_epoch=1,
        validation_file=val_id.get("id"),
        suffix="sports",
        batch_size=4,
        compute_classification_metrics=True,
        classification_n_classes=2,
        classification_positive_class="hockey",
        classification_betas=[0.5, 1, 2],
        prompt_loss_weight=0.01,
        model_name="curie",
        learning_rate_multiplier=1.0,
    )
    print("#" * 5, end="\n\n")
    print(type(openai.FineTune.retrieve(job_id.get("id"))))
    print(openai.FineTune.retrieve(job_id.get("id")))
