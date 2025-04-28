import os
from celery import shared_task

from src.config import create_app
from src.services.classify_file import classify_file


flask_app = create_app()
celery_app = flask_app.extensions["celery"]


@shared_task()
def classify_file_task(file_bytes: bytes, filename: str) -> str:
    return classify_file(file_bytes, filename)


@shared_task()
def classify_folder_task(folder_path: str) -> list[dict]:
    """
    Batch document classification. Handles folders of documents or bulk uploads asynchronously.
    """
    ...
