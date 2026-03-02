import numpy as np
import cv2
import config.fft_analyzer_config as config

def compute_high_freq_ratio(magnitude_log: np.ndarray, rows: int, cols: int, high_freq_cutoff: float) -> float:
    """
    Computes the ratio of high-frequency energy to total energy in the log-magnitude spectrum.
    Args:
        magnitude_log: Log-magnitude spectrum of the image.
        rows: Number of rows in the spectrum.
        cols: Number of columns in the spectrum.
        high_freq_cutoff: Normalized cutoff for high-frequency region (0-1).
    Returns:
        Ratio of high-frequency energy to total energy.
    """
    center_r, center_c = rows // 2, cols // 2
    Y, X = np.ogrid[:rows, :cols]
    dist = np.sqrt((X - center_c) ** 2 + (Y - center_r) ** 2)
    max_dist = np.sqrt(center_r ** 2 + center_c ** 2)
    dist_norm = dist / max_dist
    total_energy = np.sum(magnitude_log ** 2)
    if total_energy == 0:
        return 0.0
    high_freq_mask = dist_norm > high_freq_cutoff
    high_freq_energy = np.sum((magnitude_log * high_freq_mask) ** 2)
    return float(high_freq_energy / total_energy)

def count_peaks(signal: np.ndarray, peak_threshold: float) -> int:
    """
    Counts the number of peaks in a 1D signal above a specified threshold.
    Args:
        signal: Input 1D array.
        peak_threshold: Number of standard deviations above the mean to consider as a peak.
    Returns:
        Number of detected peaks in the signal.
    """
    if len(signal) == 0:
        return 0
    mean_val = np.mean(signal)
    std_val = np.std(signal)
    if std_val == 0:
        return 0
    threshold = mean_val + peak_threshold * std_val
    peaks = 0
    above = False
    for val in signal:
        if val > threshold and not above:
            peaks += 1
            above = True
        elif val <= threshold:
            above = False
    return peaks
