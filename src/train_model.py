import os
import argparse
from src.classifiers.text_classifier import TextClassifier


def train_model(num_samples: int, epochs: int, batch_size: int):
    classifier = TextClassifier()
    classifier.train(num_samples=num_samples, epochs=epochs, batch_size=batch_size)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train classification model.")
    parser.add_argument(
        "--num_samples", type=int, default=int(os.getenv("NUM_SAMPLES", 1000))
    )
    parser.add_argument("--epochs", type=int, default=int(os.getenv("EPOCHS", 2)))
    parser.add_argument(
        "--batch_size", type=int, default=int(os.getenv("BATCH_SIZE", 8))
    )
    args = parser.parse_args()

    train_model(
        num_samples=args.num_samples, epochs=args.epochs, batch_size=args.batch_size
    )
