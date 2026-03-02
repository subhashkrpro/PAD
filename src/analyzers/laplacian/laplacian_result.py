from dataclasses import dataclass

@dataclass
class LaplacianResult:
    """Laplacian variance analysis ka result."""
    score: float              # 0.0 (real/sharp) to 1.0 (fake/blurry)
    variance: float           # Laplacian variance value
    mean_gradient: float      # Mean gradient magnitude
    edge_density: float       # Edge pixels ka ratio
    local_variance_std: float # Local variance ki consistency
    details: str
