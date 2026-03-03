import cv2
import numpy as np
from src.config import moire_config

def detect_periodic_patterns(image: np.ndarray) -> float:
    """
    Detects periodic patterns in an image using autocorrelation in the frequency domain.
    Args:
        image: Input BGR image (OpenCV format).
    Returns:
        Normalized strength (0-1) of the strongest periodic pattern detected.
    """
    if len(image.shape) == 3:
        if image.shape[2] == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
        else:
            # Already single-channel 3D array
            gray = image[:, :, 0].astype(np.float32)
    else:
        # Already grayscale 2D array
        gray = image.astype(np.float32)
    scale = 256.0 / max(gray.shape)
    if scale < 1.0:
        gray = cv2.resize(gray, None, fx=scale, fy=scale)
    gray -= np.mean(gray)
    fft = np.fft.fft2(gray)
    power_spectrum = np.abs(fft) ** 2
    autocorr = np.real(np.fft.ifft2(power_spectrum))
    autocorr = autocorr / autocorr[0, 0] if autocorr[0, 0] != 0 else autocorr
    rows, cols = autocorr.shape
    center_mask = np.ones_like(autocorr, dtype=bool)
    cr, cc = rows // 2, cols // 2
    mask_size = min(rows, cols) // moire_config.AUTOCORR_MASK_DIVISOR
    center_mask[:mask_size, :mask_size] = False
    center_mask[:mask_size, -mask_size:] = False
    center_mask[-mask_size:, :mask_size] = False
    center_mask[-mask_size:, -mask_size:] = False
    masked_autocorr = autocorr * center_mask
    max_secondary = float(np.max(np.abs(masked_autocorr)))
    return min(max_secondary, 1.0)
