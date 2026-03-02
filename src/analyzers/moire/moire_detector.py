"""
Moiré Pattern Detector
=======================
When a photograph of a screen or display is taken, interference occurs between the camera sensor and the pixel grid of the screen. This results in the formation of Moiré patterns, which appear as wavy, rainbow-like artifacts.

Detection approach:
1. Convert the image to the frequency domain
2. Search for periodic patterns in specific frequency bands
3. Analyze color channels, as Moiré patterns often contain color artifacts
4. Isolate the Moiré frequency range using band-pass filtering
"""

import numpy as np
from .result import MoireResult
from .bandpass import detect_moire_bandpass
from .color_artifacts import detect_color_artifacts
from .periodic import detect_periodic_patterns
from .single_channel import analyze_single_channel
from .score import compute_score
from src.config import moire_config


class MoireDetector:
    """
    Moiré pattern detector for recaptured image detection.
    """
    def __init__(self):
        pass


    def analyze(self, image: np.ndarray) -> MoireResult:
        """
        Detects Moiré patterns in an image.
        Args:
            image: BGR image (OpenCV format)
        Returns:
            MoireResult with score and details
        """
        if len(image.shape) != 3:
            moire_intensity = analyze_single_channel(image)
            return MoireResult(
                score=min(moire_intensity * 0.5, 1.0),
                moire_intensity=moire_intensity,
                color_artifact_score=0.0,
                periodic_strength=moire_intensity,
                details="Grayscale image - limited Moiré analysis",
            )

        moire_intensity = detect_moire_bandpass(image)
        color_artifact_score = detect_color_artifacts(image)
        periodic_strength = detect_periodic_patterns(image)
        score = compute_score(moire_intensity, color_artifact_score, periodic_strength)
        details = (
            f"Moiré Analysis: intensity={moire_intensity:.4f}, "
            f"color_artifacts={color_artifact_score:.4f}, "
            f"periodic_strength={periodic_strength:.4f}, "
            f"score={score:.3f}"
        )
        return MoireResult(
            score=score,
            moire_intensity=moire_intensity,
            color_artifact_score=color_artifact_score,
            periodic_strength=periodic_strength,
            details=details,
        )

