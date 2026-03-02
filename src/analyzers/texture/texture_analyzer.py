"""
Texture Analysis Module
========================
Analyze image texture properties to distinguish between genuine and recaptured images.

Techniques used:
1. GLCM (Gray-Level Co-occurrence Matrix) - Texture features
2. LBP (Local Binary Pattern) - Micro-texture patterns
3. Gabor Filters - Multi-scale texture analysis

In recaptured images:
- Texture smoothness is higher
- LBP patterns tend to be uniform (due to screen pixel grid)
- Specific orientations dominate in Gabor filter responses
"""


import cv2
import numpy as np
from .result import TextureResult
from .glcm import compute_glcm_features
from .lbp import compute_lbp_uniformity
from .gabor import compute_gabor_features
from .score import compute_score
from config import texture_config


class TextureAnalyzer:
    """
    Texture-based recaptured image detector.
    """
    def __init__(self):
        pass

    def analyze(self, image: np.ndarray) -> TextureResult:
        """
        Analyze the texture properties of an image.
        Args:
            image: BGR image (OpenCV format)
        Returns:
            TextureResult with score and details
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        target_size = texture_config.TARGET_SIZE
        h, w = gray.shape
        scale = target_size / max(h, w)
        if scale < 1.0:
            gray = cv2.resize(gray, None, fx=scale, fy=scale)
        glcm_contrast, glcm_homogeneity, glcm_energy, glcm_correlation = compute_glcm_features(gray)
        lbp_uniformity = compute_lbp_uniformity(gray)
        gabor_variance = compute_gabor_features(gray)
        score = compute_score(
            glcm_contrast, glcm_homogeneity, glcm_energy,
            glcm_correlation, lbp_uniformity, gabor_variance,
        )
        details = (
            f"Texture Analysis: GLCM(contrast={glcm_contrast:.2f}, "
            f"homogeneity={glcm_homogeneity:.4f}, energy={glcm_energy:.4f}, "
            f"correlation={glcm_correlation:.4f}), "
            f"LBP_uniformity={lbp_uniformity:.4f}, "
            f"gabor_variance={gabor_variance:.4f}, score={score:.3f}"
        )
        return TextureResult(
            score=score,
            glcm_contrast=glcm_contrast,
            glcm_homogeneity=glcm_homogeneity,
            glcm_energy=glcm_energy,
            glcm_correlation=glcm_correlation,
            lbp_uniformity=lbp_uniformity,
            gabor_variance=gabor_variance,
            details=details,
        )

