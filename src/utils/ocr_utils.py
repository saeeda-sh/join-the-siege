import cv2
import numpy as np


def ocr_image_processing(image: np.ndarray) -> np.ndarray:
    """
    Image processing before extracting text from image using OCR.
    """
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    grey = cv2.GaussianBlur(grey, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    kernel = np.ones((3, 3), np.uint8)
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return processed
