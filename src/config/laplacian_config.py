"""
Laplacian Variance Analyzer Configuration
=========================================
All hardcoded values for LaplacianVarianceAnalyzer are defined here.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class LaplacianConfig:
    blur_threshold: float = 100.0
    sharp_threshold: float = 500.0
    block_size: int = 64
    sobel_ksize: int = 3
    canny_lower_factor: float = 0.67
    canny_upper_factor: float = 1.33
    # Score weights/thresholds
    variance_very_blurry: float = 50.0
    variance_blurry: float = 100.0
    variance_soft: float = 200.0
    mean_gradient_low: float = 10.0
    mean_gradient_soft: float = 20.0
    edge_density_very_low: float = 0.01
    edge_density_low: float = 0.03
    local_var_std_uniform: float = 20.0
    local_var_std_varied: float = 80.0
    # Score increments
    score_var_very_blurry: float = 0.15
    score_var_blurry: float = 0.10
    score_var_soft: float = 0.05
    score_grad_low: float = 0.12
    score_grad_soft: float = 0.05
    score_edge_very_low: float = 0.10
    score_edge_low: float = 0.05
    score_local_uniform: float = 0.10
    score_local_varied: float = 0.05
