# Modules

This document details the core modules responsible for authenticity detection in the Photo Authenticity Detector.

## Analyzers (`src/analyzers/`)

### 1. FFT Analyzer (`fft/`)
The Fast Fourier Transform (FFT) Analyzer works in the frequency domain. When photographing a digital screen or a printed poster, the grid layout (pixels or print dots) creates high-frequency periodic patterns.
- **Process**: Converts image to grayscale $\rightarrow$ Applies FFT $\rightarrow$ Computes magnitude spectrum.
- **Key Features Detected**:
  - `high_freq_ratio`: Proportion of high-frequency energy. Screens typically have sharper frequency cutoffs or specific spikes.
  - `spectral_peaks`: Identifies abnormally regular peaks in the spectrum.
  - `gradient_kurtosis`: Measures the distribution of image gradients.

### 2. Moiré Detector (`moire/`)
Moiré patterns are interference patterns that appear when a camera's sensor grid overlaps with a screen's pixel grid.
- **Process**: Multi-step analysis including color artifact detection and band-pass filtering.
- **Key Features Detected**:
  - `moire_intensity`: Strength of targeted frequencies.
  - `color_artifact_score`: Screens often produce rainbow-like color artifacts when photographed.
  - `periodic_strength`: Measures the strength of recurring wave-like patterns.

### 3. Laplacian Variance Analyzer (`laplacian/`)
This analyzer measures the "blurriness" or "sharpness" of an image. Recaptured images (especially photos of screens) often lose high-frequency crispness and appear slightly out of focus.
- **Process**: Applies the Laplacian operator to the image.
- **Key Features Detected**:
  - `global_variance`: Overall variance of the Laplacian. Higher variance = sharper image.
  - `local_variance_mean`: Analyzes variance in local patches to detect uniform blur vs. depth-of-field blur.
  - `variance_std`: Consistency of sharpness across the image.

### 4. Texture Analyzer (`texture/`)
Analyzes micro-textures. Screens and paper have distinct physical micro-textures compared to real-world objects.
- **Process**: Uses three different texture descriptors: GLCM, LBP, and Gabor filters.
- **Key Features Detected**:
  - `glcm_contrast`, `glcm_homogeneity`, `glcm_energy`, `glcm_correlation`: Gray-Level Co-occurrence Matrix properties. Screens often have high homogeneity at the micro-level.
  - `lbp_uniformity`: Local Binary Patterns are used to detect screen sub-pixel structures.
  - `gabor_energy_mean`, `gabor_energy_var`: Response to Gabor filters at various scales and orientations.

## Detection Core (`src/detector/`)
- **`main_detector.py`**: Contains `PhotoAuthenticityDetector`.
- **Initialization**: Configured with a dictionary of weights (how much importance to give to each analyzer) and a classification `threshold`.
- **Execution**: Takes an image array, routes it to all analyzers, and returns a detailed `DetectionResult`.

## Interfaces

### CLI (`src/cli/`)
- Uses `argparse` for command-line options.
- Supports single file analysis, batch folder analysis, verbose output, and JSON output formatting.
- Entry point logic is in `cli.py` and argument parsing in `parser.py`.

### Camera & UI (`src/camera/` & `src/gallery/`)
- Provides an OpenCV-based live camera feed.
- Calculates results on frames in real-time or at set intervals in "auto mode".
- Gallery interface for reviewing saved capture frames and their authenticity scores.
