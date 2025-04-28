import os
import joblib
import torch
from datasets import Dataset
from sklearn.preprocessing import LabelEncoder
from typing import List, Tuple
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    PreTrainedTokenizerBase,
    Trainer,
    TrainingArguments,
)

from src.classifiers.base_classifier import BaseClassifier
from src.data.data_factory import SyntheticDataFactory


class TextClassifier(BaseClassifier):
    def __init__(
        self,
        model_name="distilbert-base-uncased",
        num_labels: int = 3,
        load_from_path: str = None,
    ):
        """
        Initializes the TextClassifier by inheriting from BaseClassifier.

        Args:
            model_name (str): The name of the pre-trained model.
            num_labels (int): The number of classification labels.
            load_from_path (str): Path to load a trained model from.
        """
        super().__init__(
            model_name=model_name,
            load_from_path=load_from_path,
            model=AutoModelForSequenceClassification,
            processor=AutoTokenizer,
            num_labels=num_labels,
        )

        if load_from_path:
            self.load(path_or_name=load_from_path)

    def preprocessing(
        self, texts: List[str], labels: List[str], tokenizer: PreTrainedTokenizerBase
    ) -> Tuple[Dataset, LabelEncoder]:
        """
        Creates dataset by combining tokenized inputs with labels
        """
        label_encoder = LabelEncoder()
        encoded_labels = label_encoder.fit_transform(labels)

        encodings = tokenizer(texts, truncation=True, padding=True)
        encodings["labels"] = encoded_labels
        dataset = Dataset.from_dict(encodings)

        return dataset, label_encoder

    def predict(self, text: str) -> str:
        inputs = self.processor(
            text, return_tensors="pt", truncation=True, padding=True
        )

        with torch.no_grad():
            logits = self.model(**inputs).logits
        predicted_class_id = torch.argmax(logits, dim=1).item()

        if not self.label_encoder:
            raise ValueError("Label encoder not loaded.")

        return self.label_encoder.inverse_transform([predicted_class_id])[0]

    def train(self, num_samples=1000, epochs=3, batch_size=8):
        # Load or generate dataset
        dataset, label_encoder = self.load_synthetic_data(num_samples)
        self.label_encoder = label_encoder

        # Split into train and test datasets
        train_size = int(0.8 * len(dataset))
        train_dataset = dataset.select(range(train_size))
        test_dataset = dataset.select(range(train_size, len(dataset)))

        training_args = self.configure_training_args(epochs, batch_size)

        # Trainer setup
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset,
            processing_class=self.processor,
        )
        trainer.train()

        # Save the trained model and tokenizer
        self.save("model/")

    def load_synthetic_data(
        self,
        num_samples: int,
    ) -> Tuple[Dataset, LabelEncoder]:
        """
        Generates new synthetic data and encodes it.
        """
        factory = SyntheticDataFactory(num_samples=num_samples)
        texts, labels = factory.generate()
        dataset, label_encoder = self.preprocessing(texts, labels, self.processor)
        return dataset, label_encoder

    def configure_training_args(
        self, epochs: int, batch_size: int
    ) -> TrainingArguments:
        return TrainingArguments(
            output_dir="./results",
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir="./logs",
            logging_steps=10,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
        )
