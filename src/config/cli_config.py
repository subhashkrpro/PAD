"""
Configuration for CLI options and defaults
"""

DEFAULT_THRESHOLD = 0.12
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp"}
PROGRAM_NAME = "photo-auth-detector"
DESCRIPTION = (
    "Photo Authenticity Detector - Detect real photos vs recaptured images "
    "(screen/mobile/poster photos) using FFT, Moiré patterns, "
    "Laplacian Variance, and Texture Analysis."
)
EPILOG = """
Examples:
  uv run detect photo.jpg
  uv run detect photo.jpg --verbose  
  uv run detect ./photos/ --batch
  uv run detect photo.jpg --threshold 0.5
"""
BATCH_SUMMARY_LINE = "\n  Batch Summary: {count} images processed"
HEADER_LINES = [
    "=" * 60,
    "  PHOTO AUTHENTICITY DETECTOR",
    "  FFT | Moiré | Laplacian | Texture Analysis",
    "=" * 60,
]
