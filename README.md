# Photo Authenticity Detector

This tool detects whether a photo is a real live capture or a recaptured image from a screen, mobile, or poster.

This project uses various signal processing and computer vision techniques to analyze an image and determine its authenticity. It identifies artifacts distinct to screens and prints that are not present in the natural world.

## Features

| Analyzer | What it Detects (Kya Detect Karta Hai) |
|----------|---------------------|
| **FFT Analysis** | Screen pixel grid patterns in the frequency domain. |
| **Moiré Detection** | Camera-screen interference patterns (wavy/rainbow colors). |
| **Laplacian Variance** | Blur level (recaptured images tend to suffer from generation loss and are softer). |
| **Texture Analysis** | Micro-texture uniformities typical of screens/paper using GLCM, LBP, and Gabor filters. |

## Quick Start (Setup)

Ensure you have [uv](https://github.com/astral-sh/uv) installed, then run:

```bash
# Project setup
git clone https://github.com/subhashkrpro/PAD
cd PAD

uv sync

# Run the interactive menu (Includes Live Camera, Gallery, and Analysis)
uv run python main.py
```

## CLI Usage

You can also run the detector directly from the command line:

```bash
# Analyze a single image
uv run detect photo.jpg

# Detailed verbose output
uv run detect photo.jpg --verbose

# Output machine-readable JSON
uv run detect photo.jpg --json

# Batch mode - Analyze all images in a folder
uv run detect ./photos/ --batch

# Use a custom decision threshold (Default is 0.12)
uv run detect photo.jpg --threshold 0.5
```

## Camera Usage

Use your webcam to detect real vs recaptured photos live.

```bash
# Start live camera detection
uv run camera

# Start in auto-capture mode
uv run camera --auto

# Capture a single photo, analyze, and exit
uv run camera --capture-only

# Use a different camera device (e.g., /dev/video1 or index 1)
uv run camera --device 1
```

## Documentation

For a deep dive into the underlying architecture, workflows, and specifics of the algorithms used, please check the detailed documentation located in the `docs/` folder:

*   **[Architecture](docs/architecture.md)**: High-level design and components.
*   **[Modules](docs/modules.md)**: Detailed breakdown of the signal processing analyzers (FFT, Moiré, etc.).
*   **[Workflow](docs/workflow.md)**: Control flow of the CLI, camera, and backend.
*   **[Features & Limitations](docs/features_limitations.md)**: What this tool excels at and where it falls short.
