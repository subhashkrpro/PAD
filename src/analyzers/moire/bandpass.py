import cv2
import numpy as np
from src.config.moire_config import BANDPASS_LOW, BANDPASS_HIGH

def detect_moire_bandpass(image: np.ndarray, bandpass_low=BANDPASS_LOW, bandpass_high=BANDPASS_HIGH) -> float:
    """
    Detects moiré patterns in an image using a bandpass filter in the frequency domain.
    Args:
        image: Input BGR image (OpenCV format).
        bandpass_low: Lower normalized cutoff for the bandpass filter.
        bandpass_high: Upper normalized cutoff for the bandpass filter.
    Returns:
        Ratio of bandpass-filtered energy to total energy in the frequency domain.
    """
    if len(image.shape) == 3:
        if image.shape[2] == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
        else:
            gray = image[:, :, 0].astype(np.float32)
    else:
        gray = image.astype(np.float32)
    rows, cols = gray.shape
    dft = np.fft.fft2(gray)
    dft_shift = np.fft.fftshift(dft)
    center_r, center_c = rows // 2, cols // 2
    max_radius = min(center_r, center_c)
    Y, X = np.ogrid[:rows, :cols]
    dist = np.sqrt((X - center_c) ** 2 + (Y - center_r) ** 2) / max_radius
    bandpass_mask = ((dist >= bandpass_low) & (dist <= bandpass_high)).astype(np.float32)
    bandpass_mask = cv2.GaussianBlur(bandpass_mask, (5, 5), 1.0)
    filtered = dft_shift * bandpass_mask
    magnitude = np.abs(filtered)
    total_mag = np.sum(np.abs(dft_shift))
    if total_mag == 0:
        return 0.0
    bandpass_energy = float(np.sum(magnitude) / total_mag)
    return bandpass_energy
