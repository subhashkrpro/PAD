from src.config.moire_config import (
    MOIRE_INTENSITY_THRESHOLDS, MOIRE_INTENSITY_SCORES,
    COLOR_ARTIFACT_THRESHOLDS, COLOR_ARTIFACT_SCORES,
    PERIODIC_STRENGTH_THRESHOLDS, PERIODIC_STRENGTH_SCORES
)

def compute_score(moire_intensity: float, color_artifact_score: float, periodic_strength: float) -> float:
    score = 0.0
    # Moiré intensity
    if moire_intensity > MOIRE_INTENSITY_THRESHOLDS[0]:
        score += MOIRE_INTENSITY_SCORES[0]
    elif moire_intensity > MOIRE_INTENSITY_THRESHOLDS[1]:
        score += MOIRE_INTENSITY_SCORES[1]
    # Color artifacts
    if color_artifact_score > COLOR_ARTIFACT_THRESHOLDS[0]:
        score += COLOR_ARTIFACT_SCORES[0]
    elif color_artifact_score > COLOR_ARTIFACT_THRESHOLDS[1]:
        score += COLOR_ARTIFACT_SCORES[1]
    elif color_artifact_score > COLOR_ARTIFACT_THRESHOLDS[2]:
        score += COLOR_ARTIFACT_SCORES[2]
    # Periodic patterns
    if periodic_strength > PERIODIC_STRENGTH_THRESHOLDS[0]:
        score += PERIODIC_STRENGTH_SCORES[0]
    elif periodic_strength > PERIODIC_STRENGTH_THRESHOLDS[1]:
        score += PERIODIC_STRENGTH_SCORES[1]
    return min(score, 1.0)
