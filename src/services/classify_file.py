from src.classifiers.text_classifier import TextClassifier
from src.utils.parsers import extract_text_from_file


text_classifier = TextClassifier(load_from_path="model/")


def classify_file(file_bytes: bytes, filename: str) -> str:
    filename = filename.lower()
    ext = filename.rsplit(".", 1)[-1].lower()

    try:
        text = extract_text_from_file(file_bytes, ext)
        label = text_classifier.predict(text)
        return label
    except Exception as e:
        return f"Error: {str(e)}"
