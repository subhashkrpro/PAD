from dataclasses import dataclass

@dataclass
class MoireResult:
    """The Result of Moiré pattern detection."""
    score: float                # 0.0 (no moiré) to 1.0 (strong moiré)
    moire_intensity: float      # Moiré pattern ki intensity
    color_artifact_score: float # Color artifacts ka score
    periodic_strength: float    # Periodic pattern ki strength
    details: str
