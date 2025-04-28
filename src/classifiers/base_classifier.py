import os
import joblib
from abc import ABC, abstractmethod


class BaseClassifier(ABC):
    def __init__(self, model_name, load_from_path=None, model=None, processor=None):
        self.model_name = model_name
        self.model = model
        self.processor = processor
        self.label_encoder = None

        self.load(load_from_path or model_name)

    @abstractmethod
    def preprocessing(self, inputs, labels):
        pass

    @abstractmethod
    def predict(self, input):
        pass

    def save(self, path: str):
        self.model.save_pretrained(path)
        self.processor.save_pretrained(path)

        if self.label_encoder:
            joblib.dump(self.label_encoder, f"{path}/label_encoder.joblib")

    def load(self, path_or_name: str = None):
        """
        Tries to load the model and processor locally, ideally this would be stored in the cloud.
        If the model isn't available locally, it loads the pre-trained model from Hugging Face.

        Args:
            path_or_name (str): Path to the local model or the model name from Hugging Face.
        """
        try:
            if os.path.exists(path_or_name):
                self.model = self.model.from_pretrained(path_or_name)
                self.processor = self.processor.from_pretrained(path_or_name)

                label_encoder_path = os.path.join(path_or_name, "label_encoder.joblib")
                if not os.path.exists(label_encoder_path):
                    raise FileNotFoundError(
                        f"Label encoder file not found at: {label_encoder_path}"
                    )
                self.label_encoder = joblib.load(label_encoder_path)

            else:
                self.model = self.model.from_pretrained(path_or_name)
                self.processor = self.processor.from_pretrained(path_or_name)
        except Exception as e:
            print(f"Error: Unable to load model. {e}")
