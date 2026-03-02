from dataclasses import dataclass, field
from analyzers.fft.fft_analyzer import FFTResult
from analyzers.moire.moire_detector import MoireResult
from analyzers.laplacian.laplacian_result import LaplacianResult
from analyzers.texture.texture_analyzer import TextureResult

@dataclass
class DetectionResult:
    verdict: str
    confidence: float
    final_score: float
    fft_result: FFTResult
    moire_result: MoireResult
    laplacian_result: LaplacianResult
    texture_result: TextureResult
    details: dict = field(default_factory=dict)

    def summary(self) -> str:
        lines = [
            "=" * 60,
            "  PHOTO AUTHENTICITY DETECTION RESULT",
            "=" * 60,
            "",
            f"  Verdict:    {self.verdict}",
            f"  Confidence: {self.confidence:.1%}",
            f"  Score:      {self.final_score:.3f} (0=Real, 1=Recaptured)",
            "",
            "-" * 60,
            "  INDIVIDUAL ANALYZER SCORES",
            "-" * 60,
            f"  FFT Analysis:        {self.fft_result.score:.3f}",
            f"  Moiré Detection:     {self.moire_result.score:.3f}",
            f"  Laplacian Variance:  {self.laplacian_result.score:.3f}",
            f"  Texture Analysis:    {self.texture_result.score:.3f}",
            "",
            "-" * 60,
            "  DETAILED METRICS",
            "-" * 60,
            f"  FFT high_freq_ratio:   {self.fft_result.high_freq_ratio:.4f}",
            f"  FFT spectral_slope:    {self.fft_result.spectral_slope:.4f}",
            f"  FFT grad_kurtosis:     {self.fft_result.gradient_kurtosis:.2f}",
            f"  FFT spectral_peaks:    {self.fft_result.spectral_peaks}",
            f"  Moiré intensity:       {self.moire_result.moire_intensity:.4f}",
            f"  Moiré color_artifacts: {self.moire_result.color_artifact_score:.4f}",
            f"  Laplacian variance:    {self.laplacian_result.variance:.2f}",
            f"  Laplacian edge_dens:   {self.laplacian_result.edge_density:.4f}",
            f"  GLCM contrast:         {self.texture_result.glcm_contrast:.2f}",
            f"  LBP uniformity:        {self.texture_result.lbp_uniformity:.4f}",
            f"  Gabor variance:        {self.texture_result.gabor_variance:.4f}",
            "=" * 60,
        ]
        return "\n".join(lines)
