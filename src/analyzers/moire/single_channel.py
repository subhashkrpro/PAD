import numpy as np
from src.config.moire_config import BANDPASS_LOW, BANDPASS_HIGH

def analyze_single_channel(gray: np.ndarray, bandpass_low=BANDPASS_LOW, bandpass_high=BANDPASS_HIGH) -> float:
    """
    Analyzes a single-channel (grayscale) image for moiré patterns using a bandpass filter in the frequency domain.
    Args:
        gray: Grayscale image array.
        bandpass_low: Lower normalized cutoff for the bandpass filter.
        bandpass_high: Upper normalized cutoff for the bandpass filter.
    Returns:
        Ratio of bandpass-filtered energy to total energy in the frequency domain.
    """
    gray_f = gray.astype(np.float32)
    dft = np.fft.fft2(gray_f)
    dft_shift = np.fft.fftshift(dft)
    rows, cols = gray.shape[:2]
    center_r, center_c = rows // 2, cols // 2
    max_radius = min(center_r, center_c)
    Y, X = np.ogrid[:rows, :cols]
    dist = np.sqrt((X - center_c) ** 2 + (Y - center_r) ** 2) / max_radius
    bandpass_mask = ((dist >= bandpass_low) & (dist <= bandpass_high)).astype(np.float32)
    filtered = dft_shift * bandpass_mask
    total_mag = np.sum(np.abs(dft_shift))
    if total_mag == 0:
        return 0.0
    return float(np.sum(np.abs(filtered)) / total_mag)
