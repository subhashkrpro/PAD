# Workflow and Control Flow

This document outlines the step-by-step execution flow of the Photo Authenticity Detector.

## 1. Entry and Dispatch (`main.py`)
When a user runs the application (`uv run python main.py`), the `entry()` function in `main.py` presents a menu with options:
1. Analyze RECENT captures
2. Analyze a SINGLE image
3. Analyze a CUSTOM folder
4. Live camera detection
5. Camera auto-detection mode
6. Quick photo capture & analyze
7. Browse Gallery
8. Manual command (advanced)

Depending on the choice, the application delegates to the respective module (`src.cli` or `src.camera` or `src.gallery`).

## 2. CLI Workflow (`src/cli/cli.py`)
For single or batch image analysis:
1. Arguments are parsed from the command line (`--threshold`, `--verbose`, `--batch`, input path).
2. `PhotoAuthenticityDetector` is instantiated with the specified configuration.
3. If batch mode is active, the system iterates over all valid images in the folder.
4. `analyze_single()` is called for each image:
   - Evaluates the image via `detector.detect(path)`.
   - Prints the result in standard or JSON format.
5. In batch mode, a summary of `REAL` vs `RECAPTURED` counts is printed at the end.

## 3. Live Camera Workflow (`src/camera/live_detector.py`)
For live camera detection:
1. The camera is initialized (`cv2.VideoCapture`).
2. A continuous loop reads frames from the camera.
3. If `auto` mode is on, a frame is automatically extracted and analyzed every `interval` seconds (configurable).
4. If the user presses `SPACE`, the current frame is captured and analyzed.
5. The `PhotoAuthenticityDetector.detect_from_array()` method performs the analysis on the memory buffer.
6. The verdict and confidence score are overlaid directly on the live video feed.

## 4. Detection Engine Workflow (`src/detector/main_detector.py`)
This is the core computational flow:
1. The detector receives an image (either a file path or an `np.ndarray`).
2. **Preprocessing**: The image is dimensionally clamped to `MAX_DIM` preserving the aspect ratio. This speeds up processing for huge images.
3. **Parallel Analysis Simulation**: The image is passed sequentially to all 4 main analyzers:
   - `fft_result = fft_analyzer.analyze(image)`
   - `moire_result = moire_detector.analyze(image)`
   - `laplacian_result = laplacian_analyzer.analyze(image)`
   - `texture_result = texture_analyzer.analyze(image)`
4. **Scoring**: A weighted sum of the individual scores is calculated.
   $$ \text{Final Score} = \sum (\text{weight}_i \times \text{score}_i) $$
5. **Verdict Generation**:
   - If `Final Score` >= `threshold`, Verdict = `RECAPTURED`
   - Else, Verdict = `REAL`
6. **Confidence Calculation**: A normalized confidence percentage indicating how far the score is from the threshold.
7. Return `DetectionResult`.
