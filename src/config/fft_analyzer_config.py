"""
FFT Analyzer Configuration
=========================
All tunable parameters for FFTAnalyzer are defined here.
Modify these values to calibrate the analyzer for your use case.
"""

# Threshold for detecting spectral peaks (std devs above mean)
PEAK_THRESHOLD = 2.5

# Cutoff ratio for high vs low frequency separation (0-1)
HIGH_FREQ_CUTOFF = 0.25

# FFT processing parameters
SOBEL_KSIZE = 3
EPSILON = 1e-6
KURTOSIS_NORMALIZATION = 3.0

# Mask radius divisor for DC component ignore (used in periodic peak detection)
MASK_RADIUS_DIVISOR = 20

# Spectral slope parameters
SPECTRAL_SLOPE_MIN_RADIUS = 10
DEFAULT_SLOPE = -0.20
RADIAL_START_RADIUS = 2
RING_WIDTH = 0.5
MIN_RADIAL_POINTS = 10
LOG_EPSILON = 1e-10

# Slope thresholds for scoring
SCORE_SLOPE_THRESHOLDS = {
    'very_flat': -0.80,
    'moderately_flat': -1.30,
    'slightly_flat': -1.45,
}

# Kurtosis thresholds for scoring
SCORE_KURTOSIS_THRESHOLDS = {
    'very_uniform': 5,
    'low': 15,
    'moderately_low': 25,
    'slightly_low': 40,
}

# Spectral peaks thresholds for scoring
SCORE_PEAKS_THRESHOLDS = {
    'high': 10,
    'medium': 5,
    'low': 3,
}

# High frequency ratio thresholds for scoring
SCORE_HFR_THRESHOLDS = {
    'low': 0.60,
    'medium': 0.75,
}
