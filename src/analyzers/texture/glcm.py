import numpy as np
from skimage.feature import graycomatrix, graycoprops
from config.texture_config import GLCM_DISTANCES, GLCM_ANGLES, GLCM_GRAY_DIV, GLCM_LEVELS

def compute_glcm_features(gray: np.ndarray) -> tuple[float, float, float, float]:
    """
    Computes texture features from a grayscale image using the Gray-Level Co-occurrence Matrix (GLCM).
    Args:
        gray: Grayscale image array.
    Returns:
        Tuple containing contrast, homogeneity, energy, and correlation features.
    """
    gray_quantized = (gray // GLCM_GRAY_DIV).astype(np.uint8)
    glcm = graycomatrix(
        gray_quantized,
        distances=GLCM_DISTANCES,
        angles=GLCM_ANGLES,
        levels=GLCM_LEVELS,
        symmetric=True,
        normed=True,
    )
    contrast = float(np.mean(graycoprops(glcm, "contrast")))
    homogeneity = float(np.mean(graycoprops(glcm, "homogeneity")))
    energy = float(np.mean(graycoprops(glcm, "energy")))
    correlation = float(np.mean(graycoprops(glcm, "correlation")))
    return contrast, homogeneity, energy, correlation
