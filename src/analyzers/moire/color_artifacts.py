import cv2
import numpy as np
from src.config.moire_config import COLOR_DIFF_THRESHOLD

def detect_color_artifacts(image: np.ndarray, color_diff_threshold=COLOR_DIFF_THRESHOLD) -> float:
    """
    Detects color artifacts in an image by analyzing differences between color channels and their Laplacian responses.
    Args:
        image: Input BGR image (OpenCV format).
        color_diff_threshold: Threshold for normalizing the mean Laplacian response.
    Returns:
        Normalized value (0-1) indicating the presence of color artifacts.
    """
    b, g, r = cv2.split(image.astype(np.float32))
    diff_rg = np.abs(r - g)
    diff_rb = np.abs(r - b)
    diff_gb = np.abs(g - b)
    lap_rg = cv2.Laplacian(diff_rg, cv2.CV_32F)
    lap_rb = cv2.Laplacian(diff_rb, cv2.CV_32F)
    lap_gb = cv2.Laplacian(diff_gb, cv2.CV_32F)
    mean_lap = (np.mean(np.abs(lap_rg)) + np.mean(np.abs(lap_rb)) + np.mean(np.abs(lap_gb))) / 3.0
    normalized = float(min(mean_lap / color_diff_threshold, 1.0))
    return normalized
