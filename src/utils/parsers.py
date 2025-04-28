import cv2
from docx import Document
from io import BytesIO
import numpy as np
import pandas as pd
from pdf2image import convert_from_path
from pypdf import PdfReader
import pytesseract

from src.utils.ocr_utils import ocr_image_processing


def extract_text_from_img(image: np.ndarray) -> str:
    custom_config = r"--oem 3 --psm 6"
    processed = ocr_image_processing(image)
    return pytesseract.image_to_string(processed, config=custom_config)


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    First, tries to parse PDF for text.
    If chars <= 20, it converts PDF to image and uses OCR to extract text.
    """
    reader = PdfReader(BytesIO(file_bytes))
    text = "\n".join([page.extract_text() or "" for page in reader.pages])

    if len(text.strip()) > 20:
        return text

    images = convert_from_path(BytesIO(file_bytes))
    ocr_text = "\n".join([extract_text_from_img(img) for img in images])
    return ocr_text


def extract_text_from_file(file_bytes: bytes, ext: str) -> str:
    """Extracts text from file based on file extension."""
    ext = ext.lower().lstrip(".")

    if ext == "pdf":
        reader = PdfReader(BytesIO(file_bytes))
        return "\n".join(
            [page.extract_text() for page in reader.pages if page.extract_text()]
        )

    elif ext in {"jpg", "jpeg", "png"}:
        # Convert image bytes to np.ndarray
        image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
        return extract_text_from_img(image)

    elif ext == ".docx":
        doc = Document(BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs])

    elif ext in {".xlsx", ".csv"}:
        df = (
            pd.read_excel(BytesIO(file_bytes))
            if ext == ".xlsx"
            else pd.read_csv(BytesIO(file_bytes))
        )
        return df.astype(str).to_string()
    else:
        raise ValueError(f"Unsupported file type. Extension: {ext}")
