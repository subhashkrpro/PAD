"""
Configuration for Moiré pattern detection.
"""

# Bandpass filter frequency range (normalized 0-0.5)
BANDPASS_LOW = 0.05
BANDPASS_HIGH = 0.45

# Color artifact detection threshold
COLOR_DIFF_THRESHOLD = 150.0

# Moiré score adjustments
GRAYSCALE_FACTOR = 0.5
AUTOCORR_MASK_DIVISOR = 8

# Moiré score thresholds
MOIRE_INTENSITY_THRESHOLDS = [0.60, 0.50]
MOIRE_INTENSITY_SCORES = [0.35, 0.20]

COLOR_ARTIFACT_THRESHOLDS = [0.40, 0.20, 0.12]
COLOR_ARTIFACT_SCORES = [0.30, 0.18, 0.08]

PERIODIC_STRENGTH_THRESHOLDS = [0.85, 0.75]
PERIODIC_STRENGTH_SCORES = [0.35, 0.20]
