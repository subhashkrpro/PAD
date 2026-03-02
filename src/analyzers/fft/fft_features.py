import numpy as np
import cv2
import src.config.fft_analyzer_config as config
from .fft_utils import count_peaks

def detect_periodic_peaks(magnitude_log: np.ndarray, rows: int, cols: int, peak_threshold: float) -> int:
    """
    Detects periodic spectral peaks in the frequency domain of an image.
    Args:
        magnitude_log: Log-magnitude spectrum of the image.
        rows: Number of rows in the spectrum.
        cols: Number of columns in the spectrum.
        peak_threshold: Threshold for peak detection.
    Returns:
        Total number of detected horizontal and vertical peaks.
    """
    center_r, center_c = rows // 2, cols // 2
    mask_radius = min(rows, cols) // config.MASK_RADIUS_DIVISOR
    magnitude_masked = magnitude_log.copy()
    cv2.circle(magnitude_masked, (center_c, center_r), mask_radius, 0, -1)
    h_line = magnitude_masked[center_r, :]
    v_line = magnitude_masked[:, center_c]
    h_peaks = count_peaks(h_line, peak_threshold)
    v_peaks = count_peaks(v_line, peak_threshold)
    return h_peaks + v_peaks

def compute_gradient_kurtosis(gray: np.ndarray) -> float:
    """
    Computes the kurtosis of the image gradient magnitude distribution.
    Args:
        gray: Grayscale image array.
    Returns:
        Kurtosis value of the gradient magnitude distribution.
    """
    gray_f = gray.astype(np.float64)
    gx = cv2.Sobel(gray_f, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray_f, cv2.CV_64F, 0, 1, ksize=3)
    grad_mag = np.sqrt(gx ** 2 + gy ** 2).ravel()
    mean_g = np.mean(grad_mag)
    std_g = np.std(grad_mag)
    if std_g < 1e-6:
        return 0.0
    kurtosis = float(np.mean(((grad_mag - mean_g) / std_g) ** 4) - 3.0)
    return kurtosis

def compute_spectral_slope(magnitude: np.ndarray, rows: int, cols: int) -> tuple[float, float]:
    """
    Computes the spectral slope and residual of the radial average in the frequency domain.
    Args:
        magnitude: Magnitude spectrum of the image.
        rows: Number of rows in the spectrum.
        cols: Number of columns in the spectrum.
    Returns:
        Tuple containing the spectral slope and the residual standard deviation.
    """
    center_r, center_c = rows // 2, cols // 2
    max_r = min(center_r, center_c) - 1
    if max_r < config.SPECTRAL_SLOPE_MIN_RADIUS:
        return -0.20, 0.0
    Y, X = np.ogrid[:rows, :cols]
    dist = np.sqrt((X - center_c) ** 2 + (Y - center_r) ** 2)
    radial_avg = []
    for r in range(2, max_r):
        ring = (dist >= r - 0.5) & (dist < r + 0.5)
        vals = magnitude[ring]
        if len(vals) > 0:
            radial_avg.append(float(np.mean(vals)))
    if len(radial_avg) < 10:
        return -0.20, 0.0
    radial = np.array(radial_avg)
    x = np.log(np.arange(1, len(radial) + 1).astype(np.float64))
    y = np.log(radial + 1e-10)
    slope, intercept = np.polyfit(x, y, 1)
    y_fit = slope * x + intercept
    residual = float(np.std(y - y_fit))
    return float(slope), residual
