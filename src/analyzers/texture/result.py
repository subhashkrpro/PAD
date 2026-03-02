from dataclasses import dataclass

@dataclass
class TextureResult:
    score: float
    glcm_contrast: float
    glcm_homogeneity: float
    glcm_energy: float
    glcm_correlation: float
    lbp_uniformity: float
    gabor_variance: float
    details: str
