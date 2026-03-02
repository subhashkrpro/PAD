"""
FFT (Fast Fourier Transform) Analyzer
======================================
Screen or poster photographs exhibit specific frequency patterns
that are not present in genuine photographs. FFT enables analysis
of images in the frequency domain.

In recaptured images:
- Regular frequency spikes appear due to the pixel grid of screens
- High frequency content is reduced (due to blur)
- Periodic patterns are observed in the frequency spectrum
"""

import cv2
import numpy as np
from src.config import fft_analyzer_config as config
from .fft_result import FFTResult
from .fft_utils import compute_high_freq_ratio
from .fft_features import detect_periodic_peaks, compute_gradient_kurtosis, compute_spectral_slope
from .fft_score import compute_score


class FFTAnalyzer:
    """
    Fast Fourier Transform based image authenticity analyzer.
    
    This module converts images to the frequency domain for analysis.
    In recaptured images, specific frequency patterns are observed due to the pixel grid of screens.
    """

    def __init__(self, peak_threshold: float = None, high_freq_cutoff: float = None):
        """
        Args:
            peak_threshold: Threshold for detecting spectral peaks (std devs above mean)
            high_freq_cutoff: Cutoff ratio for high vs low frequency separation (0-1)
                             Smaller = tighter low-freq region
        """
        self.peak_threshold = peak_threshold if peak_threshold is not None else config.PEAK_THRESHOLD
        self.high_freq_cutoff = high_freq_cutoff if high_freq_cutoff is not None else config.HIGH_FREQ_CUTOFF

    def analyze(self, image: np.ndarray) -> FFTResult:
        """
        Perform FFT analysis on the image.
        Args:
            image: BGR image (OpenCV format)
        Returns:
            FFTResult with score and details
        """
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        rows, cols = gray.shape
        optimal_rows = cv2.getOptimalDFTSize(rows)
        optimal_cols = cv2.getOptimalDFTSize(cols)
        padded = np.zeros((optimal_rows, optimal_cols), dtype=np.float32)
        padded[:rows, :cols] = gray
        dft = np.fft.fft2(padded)
        dft_shift = np.fft.fftshift(dft)
        magnitude = np.abs(dft_shift)
        magnitude_log = np.log1p(magnitude)
        high_freq_ratio = compute_high_freq_ratio(magnitude_log, optimal_rows, optimal_cols, self.high_freq_cutoff)
        spectral_peaks = detect_periodic_peaks(magnitude_log, optimal_rows, optimal_cols, self.peak_threshold)
        mean_magnitude = float(np.mean(magnitude_log))
        spectral_slope, spectral_residual = compute_spectral_slope(magnitude, optimal_rows, optimal_cols)
        gradient_kurtosis = compute_gradient_kurtosis(gray)
        score = compute_score(high_freq_ratio, spectral_peaks, mean_magnitude, spectral_slope, spectral_residual, gradient_kurtosis)
        details = (
            f"FFT Analysis: high_freq_ratio={high_freq_ratio:.4f}, "
            f"spectral_peaks={spectral_peaks}, mean_magnitude={mean_magnitude:.2f}, "
            f"slope={spectral_slope:.4f}, residual={spectral_residual:.4f}, "
            f"kurtosis={gradient_kurtosis:.2f}, score={score:.3f}"
        )
        return FFTResult(
            score=score,
            high_freq_ratio=high_freq_ratio,
            spectral_peaks=spectral_peaks,
            mean_magnitude=mean_magnitude,
            spectral_slope=spectral_slope,
            spectral_residual=spectral_residual,
            gradient_kurtosis=gradient_kurtosis,
            details=details,
        )
