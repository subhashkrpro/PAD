import numpy as np
from skimage.feature import local_binary_pattern
from config.texture_config import LBP_RADIUS, LBP_N_POINTS

def compute_lbp_uniformity(gray: np.ndarray) -> float:
    """
    Computes the uniformity score of Local Binary Pattern (LBP) features in a grayscale image.
    Args:
        gray: Grayscale image array.
    Returns:
        LBP uniformity score combining uniform pattern ratio and normalized entropy.
    """
    lbp = local_binary_pattern(
        gray,
        P=LBP_N_POINTS,
        R=LBP_RADIUS,
        method="uniform",
    )
    n_bins = LBP_N_POINTS + 2
    hist, _ = np.histogram(lbp.ravel(), bins=n_bins, range=(0, n_bins), density=True)
    uniform_ratio = float(np.sum(hist[:-1]))
    hist_nonzero = hist[hist > 0]
    entropy = -np.sum(hist_nonzero * np.log2(hist_nonzero))
    max_entropy = np.log2(n_bins)
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
    lbp_score = uniform_ratio * (1 - normalized_entropy)
    return lbp_score
