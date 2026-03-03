# Features and Limitations

## Features

The **Photo Authenticity Detector** comes packed with features to handle different use-cases for determining whether an image is a genuine photograph of the real world or a recapture (photo of a screen, printed poster, or mobile device).

1. **Multi-Algorithm Detection Engine**:
   - **FFT Analysis**: Detects frequency domain regularities.
   - **Moiré Detection**: Identifies screen-camera interference patterns.
   - **Laplacian Variance**: Measures optical blur and recaptured softness.
   - **Texture Analysis**: Evaluates GLCM, LBP, and Gabor filter responses to find micro-textures common in digital screens and printers.

2. **Versatile Interfaces**:
   - **Interactive Menu**: A user-friendly console menu to access all tools.
   - **CLI**: Supports scriptable command-line arguments for single and batch image processing.
   - **Live Camera**: A real-time OpenCV HUD that continuously analyzes camera feeds or captures photos on command.
   - **Gallery Viewer**: An interactive UI to browse past captures, view their scores, and delete false positives.

3. **Batch Processing**: Automate the analysis of thousands of photos in a folder.
4. **JSON Output**: Output machine-readable JSON for integration into other software pipelines.
5. **Adjustable Thresholds**: Tune the sensitivity (`DEFAULT_THRESHOLD`) based on your specific camera hardware or use-case.

## Limitations

While powerful, the tool relies on specific artifacts to make its decision. Some limitations apply:

1. **Reliance on Resolvable Artifacts**:
   - The detector relies heavily on seeing the screen's pixel grid or Moiré patterns. If a recaptured photo is taken from very far away or is highly compressed/downscaled, the grid patterns are lost, and the detector may classify it as a `REAL` photo.
2. **High-Quality Print Attacks**:
   - High DPI prints (e.g., professional photo paper) might lack visible grids or Moiré patterns, making them harder to detect using FFT or Texture analyzers. They might only trigger the Laplacian blur checks.
3. **Heuristic Nature**:
   - The final verdict is based on a weighted sum of heuristics. Highly unusual, genuine photos (e.g., photos of chainlink fences, window screens, or textured fabrics) might produce Moiré patterns and falsely trigger the detector (`False Positives`).
4. **Performance Overhead**:
   - The analytical pipeline (especially Gabor and FFT combinations) is CPU computationally expensive. Live camera auto-detection runs at intervals to maintain framerate.
5. **GUI Requirement**:
   - The camera and gallery modules require a windowing system (Display/GUI). They will fail in headless Docker containers or remote SSH sessions without X11 forwarding.
