# Architecture

The **Photo Authenticity Detector** is designed with a modular architecture that separates concerns between image processing (analyzers), core detection logic (detector), user interfaces (CLI, Camera UI, Gallery), and configuration.

## High-Level Architecture

The system is organized into the following main layers:

1. **User Interfaces (Entry Points)**
   - **`main.py`**: The primary entry point that routes user actions (single analysis, batch analysis, live camera, gallery view, etc.).
   - **`src/cli`**: Command Line Interface for analyzing images and folders.
   - **`src/camera`**: Interactive camera interface for live detection and photo capture.
   - **`src/gallery`**: Gallery viewer capabilities.

2. **Core Detection Layer (`src/detector`)**
   - **`PhotoAuthenticityDetector`**: The orchestrator. It receives an image, distributes it to all configured analyzers, gathers their individual scores, and computes a final weighted score.
   - **`DetectionResult`**: A structured object containing the final verdict (`REAL` or `RECAPTURED`), confidence score, and detailed results from each analyzer.

3. **Analyzers Layer (`src/analyzers`)**
   - The heart of the detection logic. This layer consists of specialized modules that look for specific artifacts indicating a recaptured photo (e.g., a photo of a screen).
   - Each analyzer implements an `analyze()` method that returns a specialized result object containing its individual score and explanation.
   - Sub-modules: `fft`, `moire`, `laplacian`, `texture`.

4. **Configuration Layer (`src/config`)**
   - Centralized configuration files for tuning thresholds, weights, camera settings, and CLI display preferences.

## Component Interaction

1. An image is provided via CLI, Camera, or Python API.
2. The image is loaded and passed to `PhotoAuthenticityDetector.detect()`.
3. The detector resizes the image if it exceeds the maximum dimension (`MAX_DIM`).
4. The image is passed sequentially to:
   - `FFTAnalyzer`
   - `MoireDetector`
   - `LaplacianVarianceAnalyzer`
   - `TextureAnalyzer`
5. Each analyzer computes its heuristics and returns an anomaly score bounded between 0.0 (Real) and 1.0 (Recaptured).
6. The detector computes a final weighted average of these scores.
7. If the final score exceeds the `detector_config.DEFAULT_THRESHOLD`, the verdict is `RECAPTURED`. Otherwise, it is `REAL`.
8. The result is formatted and presented to the user.
