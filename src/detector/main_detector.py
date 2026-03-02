"""
Photo Authenticity Detector
============================
Combines all analyzers to provide a final verdict:
- FFT Analysis (frequency domain patterns)
- Moiré Pattern Detection (screen interference)
- Laplacian Variance (blur/sharpness)
- Texture Analysis (GLCM, LBP, Gabor)

Uses a weighted scoring system for the final decision:
    REAL PHOTO  vs  RECAPTURED (photo of screen/mobile/poster)
"""

import cv2
import numpy as np
from analyzers import (
    FFTAnalyzer,
    MoireDetector,
    LaplacianVarianceAnalyzer,
    TextureAnalyzer,
)
from config import detector_config
from .result import DetectionResult

class PhotoAuthenticityDetector:
    def __init__(self, weights: dict[str, float] | None = None, threshold: float = detector_config.DEFAULT_THRESHOLD):
        """
        Initialize the authenticity detector with analyzer weights and decision threshold.
        """
        self.weights = weights or detector_config.DEFAULT_WEIGHTS.copy()
        self.threshold = threshold
        total = sum(self.weights.values())
        # Ensure weights sum to 1.0
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total:.3f}")
        # Initialize all analyzers
        self.fft_analyzer = FFTAnalyzer()
        self.moire_detector = MoireDetector()
        self.laplacian_analyzer = LaplacianVarianceAnalyzer()
        self.texture_analyzer = TextureAnalyzer()

    def detect(self, image_path: str) -> DetectionResult:
        """
        Load an image from the given path and run authenticity detection.
        Raises FileNotFoundError or ValueError if loading fails.
        """
        import os
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        # Run detection on the loaded image array
        return self.detect_from_array(image)

    def detect_from_array(self, image: np.ndarray) -> DetectionResult:
        """
        Run authenticity detection on a given image array.
        Resizes image if larger than max allowed dimension.
        Combines all analyzer scores using weights and returns the final result.
        """
        max_dim = detector_config.MAX_DIM
        h, w = image.shape[:2]
        # Resize image if necessary
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            image = cv2.resize(image, None, fx=scale, fy=scale)
        # Run all analyzers
        fft_result = self.fft_analyzer.analyze(image)
        moire_result = self.moire_detector.analyze(image)
        laplacian_result = self.laplacian_analyzer.analyze(image)
        texture_result = self.texture_analyzer.analyze(image)
        # Weighted sum for final score
        final_score = (
            self.weights["fft"] * fft_result.score
            + self.weights["moire"] * moire_result.score
            + self.weights["laplacian"] * laplacian_result.score
            + self.weights["texture"] * texture_result.score
        )
        # Decide verdict and confidence
        verdict = "RECAPTURED" if final_score >= self.threshold else "REAL"
        if final_score >= self.threshold:
            confidence = min((final_score - self.threshold) / (1.0 - self.threshold) * 0.5 + 0.5, 1.0)
        else:
            confidence = min((self.threshold - final_score) / self.threshold * 0.5 + 0.5, 1.0)
        # Return detailed result
        return DetectionResult(
            verdict=verdict,
            confidence=confidence,
            final_score=final_score,
            fft_result=fft_result,
            moire_result=moire_result,
            laplacian_result=laplacian_result,
            texture_result=texture_result,
            details={
                "weights": self.weights,
                "threshold": self.threshold,
                "image_size": f"{image.shape[1]}x{image.shape[0]}",
            },
        )
