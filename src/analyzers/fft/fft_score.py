import config.fft_analyzer_config as config

def _score_by_thresholds(value, thresholds, scores, reverse=False):
    """
    thresholds: list of threshold values (sorted ascending if reverse=False, descending if reverse=True)
    scores: list of scores to add if value crosses threshold
    reverse: if True, checks value < threshold, else value > threshold
    """
    for t, s in zip(thresholds, scores):
        if (value < t) if reverse else (value > t):
            return s
    return 0.0

def compute_score(high_freq_ratio: float, spectral_peaks: int, mean_magnitude: float, spectral_slope: float,
                  spectral_residual: float, gradient_kurtosis: float) -> float:
    score = 0.0
    # Spectral slope (flatter = more processed)
    slope_thresholds = [config.SCORE_SLOPE_THRESHOLDS[k] for k in ['very_flat','moderately_flat','slightly_flat']]
    slope_scores = [0.25, 0.18, 0.10]
    score += _score_by_thresholds(spectral_slope, slope_thresholds, slope_scores)

    # Gradient kurtosis (lower = more processed)
    kurtosis_thresholds = [config.SCORE_KURTOSIS_THRESHOLDS[k] for k in ['very_uniform','low','moderately_low','slightly_low']]
    kurtosis_scores = [0.30, 0.22, 0.12, 0.05]
    score += _score_by_thresholds(gradient_kurtosis, kurtosis_thresholds, kurtosis_scores, reverse=True)

    # Spectral peaks (higher = more processed)
    peaks_thresholds = [config.SCORE_PEAKS_THRESHOLDS[k] for k in ['high','medium','low']]
    peaks_scores = [0.15, 0.08, 0.04]
    score += _score_by_thresholds(spectral_peaks, peaks_thresholds, peaks_scores)

    # High frequency ratio (lower = more processed)
    hfr_thresholds = [config.SCORE_HFR_THRESHOLDS[k] for k in ['low','medium']]
    hfr_scores = [0.08, 0.04]
    score += _score_by_thresholds(high_freq_ratio, hfr_thresholds, hfr_scores, reverse=True)

    return min(score, 1.0)
