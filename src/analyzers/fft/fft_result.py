from dataclasses import dataclass

@dataclass
class FFTResult:
    """FFT analysis ka result."""
    score: float              # 0.0 (real) to 1.0 (fake/recaptured)
    high_freq_ratio: float    # High frequency energy ka ratio
    spectral_peaks: int       # Periodic peaks ki count
    mean_magnitude: float     # Average magnitude spectrum mein
    spectral_slope: float     # 1/f power law slope (steeper = more natural)
    spectral_residual: float  # Deviation from smooth 1/f fit
    gradient_kurtosis: float  # Gradient distribution kurtosis (natural = high)
    details: str              # Human-readable explanation
