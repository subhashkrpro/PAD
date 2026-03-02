from src.config.laplacian_config import LaplacianConfig
from .laplacian_result import LaplacianResult
from .laplacian_utils import LaplacianUtils
import numpy as np
import cv2

class LaplacianVarianceAnalyzer:
    """
    Laplacian Variance based blur/sharpness analyzer.
    Recaptured images typically exhibit blur, which is not present in genuine photographs.
    A low Laplacian variance indicates that the image is blurry.
    """
    def __init__(self, config: LaplacianConfig = LaplacianConfig()):
        self.config = config

    def analyze(self, image: np.ndarray) -> LaplacianResult:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        variance = LaplacianUtils.compute_laplacian_variance(gray)
        mean_gradient = LaplacianUtils.compute_mean_gradient(gray)
        edge_density = LaplacianUtils.compute_edge_density(gray)
        local_variance_std = LaplacianUtils.compute_local_variance_consistency(gray, self.config.block_size)
        score = self._compute_score(variance, mean_gradient, edge_density, local_variance_std)
        details = (
            f"Laplacian Analysis: variance={variance:.2f}, "
            f"mean_gradient={mean_gradient:.2f}, edge_density={edge_density:.4f}, "
            f"local_var_std={local_variance_std:.2f}, score={score:.3f}"
        )
        return LaplacianResult(
            score=score,
            variance=variance,
            mean_gradient=mean_gradient,
            edge_density=edge_density,
            local_variance_std=local_variance_std,
            details=details,
        )

    def _compute_score(self, variance, mean_gradient, edge_density, local_variance_std) -> float:
        c = self.config
        score = 0.0
        if variance < c.variance_very_blurry:
            score += c.score_var_very_blurry
        elif variance < c.variance_blurry:
            score += c.score_var_blurry
        elif variance < c.variance_soft:
            score += c.score_var_soft
        if mean_gradient < c.mean_gradient_low:
            score += c.score_grad_low
        elif mean_gradient < c.mean_gradient_soft:
            score += c.score_grad_soft
        if edge_density < c.edge_density_very_low:
            score += c.score_edge_very_low
        elif edge_density < c.edge_density_low:
            score += c.score_edge_low
        if local_variance_std < c.local_var_std_uniform:
            score += c.score_local_uniform
        elif local_variance_std < c.local_var_std_varied:
            score += c.score_local_varied
        return min(score, 1.0)
