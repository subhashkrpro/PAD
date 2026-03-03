import cv2
import numpy as np
import numpy as np
from src.config.texture_config import GABOR_FREQUENCIES, GABOR_ORIENTATIONS, GABOR_KSIZE, GABOR_SIGMA, GABOR_GAMMA, GABOR_PSI

def compute_gabor_features(gray: np.ndarray) -> float:
    """
    Computes texture features from a grayscale image using Gabor filters at multiple frequencies and orientations.
    Args:
        gray: Grayscale image array.
    Returns:
        Mean normalized variance of Gabor filter responses across all frequencies and orientations.
    """
    gray_f = gray.astype(np.float32)
    all_norm_variances = []
    for freq in GABOR_FREQUENCIES:
        orientation_means = []
        for theta in GABOR_ORIENTATIONS:
            kernel = cv2.getGaborKernel(
                ksize=GABOR_KSIZE,
                sigma=GABOR_SIGMA,
                theta=theta,
                lambd=1.0 / freq,
                gamma=GABOR_GAMMA,
                psi=GABOR_PSI,
            )
            kernel /= kernel.sum() if kernel.sum() != 0 else 1
            response = cv2.filter2D(gray_f, cv2.CV_32F, kernel)
            orientation_means.append(np.mean(np.abs(response)))
        orient_arr = np.array(orientation_means)
        mean_resp = np.mean(orient_arr)
        if mean_resp > 0:
            normalized = orient_arr / mean_resp
            all_norm_variances.append(float(np.var(normalized)))
        else:
            all_norm_variances.append(0.0)
    mean_norm_var = float(np.mean(all_norm_variances))
    return mean_norm_var
