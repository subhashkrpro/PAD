from src.config.texture_config import (
    CONTRAST_THRESHOLDS, CONTRAST_SCORES,
    HOMOGENEITY_THRESHOLDS, HOMOGENEITY_SCORES,
    ENERGY_THRESHOLDS, ENERGY_SCORES,
    LBP_THRESHOLDS, LBP_SCORES,
    GABOR_THRESHOLDS, GABOR_SCORES
)


def _score_by_thresholds(value, thresholds, scores, reverse=False):
    """
    Assigns score based on value crossing thresholds.
    thresholds: list of threshold values (ascending if reverse=False, descending if reverse=True)
    scores: list of scores to add if value crosses threshold
    reverse: if True, checks value > threshold, else value < threshold
    """
    for t, s in zip(thresholds, scores):
        if (value > t) if reverse else (value < t):
            return s
    return 0.0

def compute_score(contrast, homogeneity, energy, correlation, lbp_uniformity, gabor_variance) -> float:
    score = 0.0
    score += _score_by_thresholds(contrast, CONTRAST_THRESHOLDS, CONTRAST_SCORES)
    score += _score_by_thresholds(homogeneity, HOMOGENEITY_THRESHOLDS, HOMOGENEITY_SCORES, reverse=True)
    score += _score_by_thresholds(energy, ENERGY_THRESHOLDS, ENERGY_SCORES, reverse=True)
    score += _score_by_thresholds(lbp_uniformity, LBP_THRESHOLDS, LBP_SCORES, reverse=True)
    score += _score_by_thresholds(gabor_variance, GABOR_THRESHOLDS, GABOR_SCORES)
    return min(score, 1.0)
