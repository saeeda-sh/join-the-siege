from src.classifiers.text_classifier import TextClassifier


class FinanceClassifier(TextClassifier):
    def __init__(
        self,
        model_name="distilbert-base-uncased",
        num_labels: int = 3,
        load_from_path: str = None,
        industry: str = "finance",
    ):
        super().__init__(
            model_name=model_name,
            num_labels=num_labels,
            load_from_path=load_from_path,
            industry=industry,
        )
